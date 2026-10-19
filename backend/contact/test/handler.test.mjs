import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHandler } from '../src/handler.mjs';

const valid = { name: 'Rosa Quispe', email: 'Rosa@Ejemplo.pe', phone: '+51 999 888 777', reason: 'Alianzas', message: 'Quiero conversar sobre una alianza.', website: '' };
const ev = (body, ip = '1.2.3.4') => ({ body: JSON.stringify(body), requestContext: { http: { sourceIp: ip } }, headers: { 'user-agent': 'test' } });
const silent = { info() {}, error() {} };

function fakes({ storeFails = false, mailFails = false, sheetFails = false, allow = true } = {}) {
  const calls = { saved: [], mailed: [], rows: [] };
  return {
    calls,
    deps: {
      mode: 'live', log: silent,
      store: { save: async (m) => { if (storeFails) throw new Error('ddb'); calls.saved.push(m); } },
      mailer: { send: async (m) => { if (mailFails) throw new Error('ses'); calls.mailed.push(m); } },
      sheet: { append: async (m) => { if (sheetFails) throw new Error('sheet'); calls.rows.push(m); } },
      limiter: { allow: async () => allow },
    },
  };
}

test('mock: valida y responde 200 sin tocar ningún servicio', async () => {
  const res = await createHandler({ mode: 'mock', log: silent })(ev(valid));
  assert.equal(res.statusCode, 200);
  assert.equal(JSON.parse(res.body).mode, 'mock');
});

test('live: guarda, envía correo y agrega fila', async () => {
  const { calls, deps } = fakes();
  const res = await createHandler(deps)(ev(valid));
  assert.equal(res.statusCode, 200);
  assert.equal(calls.saved.length, 1);
  assert.equal(calls.mailed.length, 1);
  assert.equal(calls.rows.length, 1);
  assert.equal(calls.saved[0].email, 'rosa@ejemplo.pe');
  assert.equal(calls.saved[0].ip, '1.2.3.4');
});

test('live: si fallan correo y hoja, igual responde 200 porque ya se guardó', async () => {
  const { calls, deps } = fakes({ mailFails: true, sheetFails: true });
  const res = await createHandler(deps)(ev(valid));
  assert.equal(res.statusCode, 200);
  assert.equal(calls.saved.length, 1);
});

test('live: si falla DynamoDB, la Lambda falla (500 en API Gateway)', async () => {
  const { deps } = fakes({ storeFails: true });
  await assert.rejects(createHandler(deps)(ev(valid)));
});

test('honeypot lleno: responde 200 y no guarda nada', async () => {
  const { calls, deps } = fakes();
  const res = await createHandler(deps)(ev({ ...valid, website: 'http://spam' }));
  assert.equal(res.statusCode, 200);
  assert.equal(calls.saved.length, 0);
});

test('datos inválidos: 422 con los campos', async () => {
  const res = await createHandler({ mode: 'mock', log: silent })(ev({ name: 'A', email: 'x', reason: 'Nada', message: '' }));
  assert.equal(res.statusCode, 422);
  assert.deepEqual(Object.keys(JSON.parse(res.body).fields).sort(), ['email', 'message', 'name', 'reason']);
});

test('JSON roto: 400', async () => {
  const res = await createHandler({ mode: 'mock', log: silent })({ body: '{no' });
  assert.equal(res.statusCode, 400);
});

test('límite por IP: 429 y no guarda', async () => {
  const { calls, deps } = fakes({ allow: false });
  const res = await createHandler(deps)(ev(valid));
  assert.equal(res.statusCode, 429);
  assert.equal(calls.saved.length, 0);
});
