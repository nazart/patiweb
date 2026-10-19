// Lambda del formulario de contacto (API Gateway HTTP API, payload v2).
//
// MODE=mock  → valida y registra en los logs, sin escribir en ningún servicio (modo actual).
// MODE=live  → guarda en DynamoDB (fuente de verdad), y luego en paralelo envía el correo
//              por SES a info@pati.pe y agrega una fila en la hoja de Google.
//              Si fallan el correo o la hoja, el mensaje ya quedó guardado: se registra el
//              error y se responde 200 igual, para no pedirle al visitante que reenvíe.
import { randomUUID } from 'node:crypto';
import { validate } from './validate.mjs';

const json = (statusCode, body) => ({
  statusCode,
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify(body),
});

export function createHandler({ mode = 'mock', store, mailer, sheet, limiter, now = () => new Date(), log = console } = {}) {
  return async function handler(event) {
    let body;
    try {
      const raw = event?.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : event?.body;
      body = JSON.parse(raw || '{}');
    } catch {
      return json(400, { ok: false, error: 'invalid_json' });
    }

    const result = validate(body);
    if (result.bot) return json(200, { ok: true }); // honeypot: respuesta normal, sin guardar nada
    if (!result.ok) return json(422, { ok: false, error: 'validation', fields: result.errors });

    const ip = event?.requestContext?.http?.sourceIp || 'unknown';
    const msg = {
      id: randomUUID(),
      createdAt: now().toISOString(),
      ...result.data,
      ip,
      userAgent: (event?.headers?.['user-agent'] || '').slice(0, 200),
    };

    if (mode !== 'live') {
      log.info(JSON.stringify({ evt: 'contact.mock', id: msg.id, reason: msg.reason, page: msg.page }));
      return json(200, { ok: true, id: msg.id, mode: 'mock' });
    }

    if (limiter && !(await limiter.allow(ip))) return json(429, { ok: false, error: 'rate_limited' });

    await store.save(msg); // si esto falla, la Lambda responde 500 y el visitante puede reintentar

    const side = await Promise.allSettled([mailer.send(msg), sheet.append(msg)]);
    side.forEach((r, i) => {
      if (r.status === 'rejected') log.error(JSON.stringify({ evt: 'contact.side_effect_failed', target: i ? 'sheet' : 'email', id: msg.id, error: String(r.reason?.message || r.reason) }));
    });

    return json(200, { ok: true, id: msg.id });
  };
}

// Punto de entrada de la Lambda: arma las dependencias reales según el entorno.
let cached;
export const handler = async (event) => {
  if (!cached) {
    const mode = process.env.MODE || 'mock';
    const deps = { mode };
    if (mode === 'live') {
      const { makeAwsDeps } = await import('./aws.mjs');
      Object.assign(deps, await makeAwsDeps(process.env));
    }
    cached = createHandler(deps);
  }
  return cached(event);
};
