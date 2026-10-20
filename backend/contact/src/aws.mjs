// Dependencias reales para MODE=live. Solo usa el AWS SDK v3 que ya trae el runtime
// nodejs22.x de Lambda y el módulo crypto de Node: el paquete no tiene dependencias.
import { createSign } from 'node:crypto';
import { DynamoDBClient, PutItemCommand, UpdateItemCommand } from '@aws-sdk/client-dynamodb';
import { SESv2Client, SendEmailCommand } from '@aws-sdk/client-sesv2';
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';
import { claimText } from './claims.mjs';

const S = (v) => ({ S: String(v ?? '') });

export async function makeAwsDeps(env) {
  const ddb = new DynamoDBClient({});
  const ses = new SESv2Client({});
  const table = env.TABLE_NAME;

  const provider = { name: env.PROVIDER_NAME, ruc: env.PROVIDER_RUC, address: env.PROVIDER_ADDRESS };

  const store = {
    // Correlativo anual del Libro de Reclamaciones (contador atómico en DynamoDB).
    async nextClaimNumber(year) {
      const out = await ddb.send(new UpdateItemCommand({
        TableName: table,
        Key: { pk: S(`counter#claims#${year}`) },
        UpdateExpression: 'ADD seq :one',
        ExpressionAttributeValues: { ':one': { N: '1' } },
        ReturnValues: 'UPDATED_NEW',
      }));
      return Number(out.Attributes.seq.N);
    },
    // Las hojas se conservan (sin TTL): el reglamento exige guardarlas al menos 2 años.
    async saveClaim(c) {
      const item = { pk: S(`claim#${c.number}`) };
      for (const [k, v] of Object.entries(c)) item[k] = S(v);
      await ddb.send(new PutItemCommand({ TableName: table, ConditionExpression: 'attribute_not_exists(pk)', Item: item }));
    },
    async save(m) {
      await ddb.send(new PutItemCommand({
        TableName: table,
        ConditionExpression: 'attribute_not_exists(pk)',
        Item: {
          pk: S(`msg#${m.id}`), id: S(m.id), createdAt: S(m.createdAt), name: S(m.name), email: S(m.email),
          phone: S(m.phone), reason: S(m.reason), message: S(m.message), page: S(m.page), ip: S(m.ip), userAgent: S(m.userAgent),
        },
      }));
    },
  };

  const perHour = Number(env.RATE_LIMIT_PER_HOUR || 5);
  const limiter = {
    async allow(ip) {
      const hour = Math.floor(Date.now() / 3_600_000);
      const out = await ddb.send(new UpdateItemCommand({
        TableName: table,
        Key: { pk: S(`rl#${ip}#${hour}`) },
        UpdateExpression: 'ADD hits :one SET expiresAt = :ttl',
        ExpressionAttributeValues: { ':one': { N: '1' }, ':ttl': { N: String((hour + 2) * 3600) } },
        ReturnValues: 'UPDATED_NEW',
      }));
      return Number(out.Attributes.hits.N) <= perHour;
    },
  };

  const mailer = {
    async send(m) {
      const text = [
        `Nuevo mensaje desde ${m.page}`, '',
        `Nombre:  ${m.name}`, `Correo:  ${m.email}`, `Celular: ${m.phone || '—'}`, `Motivo:  ${m.reason}`, '',
        m.message, '', `ID: ${m.id} · ${m.createdAt}`,
      ].join('\n');
      await ses.send(new SendEmailCommand({
        FromEmailAddress: env.MAIL_FROM,
        Destination: { ToAddresses: [env.MAIL_TO] },
        ReplyToAddresses: [m.email],
        Content: { Simple: { Subject: { Data: `[Contacto pati.pe] ${m.reason} · ${m.name}`.slice(0, 180), Charset: 'UTF-8' }, Body: { Text: { Data: text, Charset: 'UTF-8' } } } },
      }));
    },
  };

  // Copia de la Hoja de Reclamación al consumidor (obligatoria) y aviso a Pati.
  mailer.sendClaim = async (c) => {
    await ses.send(new SendEmailCommand({
      FromEmailAddress: env.MAIL_FROM,
      Destination: { ToAddresses: [c.email], BccAddresses: [env.MAIL_TO] },
      ReplyToAddresses: [env.MAIL_TO],
      Content: { Simple: { Subject: { Data: `Hoja de Reclamación ${c.number} · Pati`, Charset: 'UTF-8' }, Body: { Text: { Data: claimText(c, provider), Charset: 'UTF-8' } } } },
    }));
  };

  const sheet = await makeSheet(env);
  return { store, limiter, mailer, sheet };
}

// Agrega una fila a la hoja de Google con una cuenta de servicio (JWT RS256 → token OAuth).
async function makeSheet(env) {
  if (!env.GOOGLE_SECRET_ARN || !env.SHEET_ID) {
    const off = async () => { throw new Error('google_not_configured'); };
    return { append: off, appendClaim: off };
  }
  const sm = new SecretsManagerClient({});
  let sa; let token = { value: '', exp: 0 };

  async function accessToken() {
    if (token.exp > Date.now() + 60_000) return token.value;
    if (!sa) sa = JSON.parse((await sm.send(new GetSecretValueCommand({ SecretId: env.GOOGLE_SECRET_ARN }))).SecretString);
    const iat = Math.floor(Date.now() / 1000);
    const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
    const unsigned = `${b64({ alg: 'RS256', typ: 'JWT' })}.${b64({ iss: sa.client_email, scope: 'https://www.googleapis.com/auth/spreadsheets', aud: 'https://oauth2.googleapis.com/token', iat, exp: iat + 3600 })}`;
    const sig = createSign('RSA-SHA256').update(unsigned).sign(sa.private_key, 'base64url');
    const res = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: `${unsigned}.${sig}` }),
    });
    if (!res.ok) throw new Error(`google_token_${res.status}`);
    const j = await res.json();
    token = { value: j.access_token, exp: Date.now() + j.expires_in * 1000 };
    return token.value;
  }

  // Evita que un texto que empiece con = + - @ se interprete como fórmula al abrir la hoja.
  const cell = (v) => (/^[=+\-@]/.test(String(v)) ? `'${v}` : String(v ?? ''));

  async function appendRow(tab, cols, row) {
    const range = encodeURIComponent(`${tab}!A:${cols}`);
    const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${env.SHEET_ID}/values/${range}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS`, {
      method: 'POST',
      headers: { authorization: `Bearer ${await accessToken()}`, 'content-type': 'application/json' },
      body: JSON.stringify({ values: [row.map(cell)] }),
    });
    if (!res.ok) throw new Error(`google_append_${res.status}`);
  }

  return {
    async appendClaim(c) {
      await appendRow('Reclamos', 'R', [c.number, c.createdAt, c.claimType, c.name, c.docType, c.docNumber, c.address, c.phone, c.email,
        c.isMinor ? `${c.guardianName} (${c.guardianDoc})` : '', c.itemType, c.amount, c.itemDescription, c.detail, c.request, 'pendiente', '', '']);
    },
    async append(m) {
      const range = encodeURIComponent(`${env.SHEET_TAB || 'Mensajes'}!A:I`);
      const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${env.SHEET_ID}/values/${range}:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS`, {
        method: 'POST',
        headers: { authorization: `Bearer ${await accessToken()}`, 'content-type': 'application/json' },
        body: JSON.stringify({ values: [[m.createdAt, m.name, m.email, m.phone, m.reason, m.message, m.page, m.id, 'nuevo'].map(cell)] }),
      });
      if (!res.ok) throw new Error(`google_append_${res.status}`);
    },
  };
}
