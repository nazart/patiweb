import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHandler } from '../src/handler.mjs';
import { validateClaim, claimText } from '../src/claims.mjs';

const valid = {
  name: 'Rosa Quispe Mamani', docType: 'DNI', docNumber: '45678912', address: 'Av. Universitaria 123, San Miguel',
  phone: '+51 999 888 777', email: 'rosa@ejemplo.pe', isMinor: false, itemType: 'servicio', amount: '0',
  itemDescription: 'Uso de la app Pati', claimType: 'reclamo', detail: 'La app no me mostró ofertas en mi pedido.',
  request: 'Que revisen mi cuenta.', accept: true, website: '',
};
const ev = (body) => ({ routeKey: 'POST /reclamos', body: JSON.stringify(body), requestContext: { http: { sourceIp: '1.2.3.4' } } });
const silent = { info() {}, error() {} };

function live({ mailFails = false } = {}) {
  let seq = 0; const saved = []; const mailed = []; const rows = [];
  return {
    saved, mailed, rows,
    handler: createHandler({
      mode: 'live', log: silent, now: () => new Date('2026-11-03T15:00:00Z'),
      limiter: { allow: async () => true },
      store: { nextClaimNumber: async () => ++seq, saveClaim: async (c) => saved.push(c), save: async () => {} },
      mailer: { send: async () => {}, sendClaim: async (c) => { if (mailFails) throw new Error('ses'); mailed.push(c); } },
      sheet: { append: async () => {}, appendClaim: async (c) => rows.push(c) },
    }),
  };
}

test('reclamo válido: número correlativo, registro, copia por correo y fila', async () => {
  const L = live();
  const r1 = JSON.parse((await L.handler(ev(valid))).body);
  const r2 = JSON.parse((await L.handler(ev({ ...valid, claimType: 'queja' }))).body);
  assert.equal(r1.number, 'LR-2026-000001');
  assert.equal(r2.number, 'LR-2026-000002');
  assert.equal(L.saved.length, 2);
  assert.equal(L.mailed.length, 2);
  assert.equal(L.rows.length, 2);
  assert.equal(r1.emailed, true);
});

test('si falla el correo, la hoja queda registrada e informa emailed=false', async () => {
  const L = live({ mailFails: true });
  const res = await L.handler(ev(valid));
  assert.equal(res.statusCode, 200);
  assert.equal(JSON.parse(res.body).emailed, false);
  assert.equal(L.saved.length, 1);
});

test('validación: documento según tipo, menor de edad con apoderado y aceptación', () => {
  assert.equal(validateClaim({ ...valid, docNumber: '123' }).errors.docNumber, 'invalid');
  assert.equal(validateClaim({ ...valid, docType: 'CE', docNumber: 'AB1234567' }).ok, true);
  const minor = validateClaim({ ...valid, isMinor: true });
  assert.equal(minor.errors.guardianName, 'required');
  assert.equal(validateClaim({ ...valid, isMinor: true, guardianName: 'Juan Quispe', guardianDoc: '12345678' }).ok, true);
  assert.equal(validateClaim({ ...valid, accept: false }).errors.accept, 'required');
  assert.equal(validateClaim({ ...valid, claimType: 'otro' }).errors.claimType, 'invalid');
  assert.equal(validateClaim({ ...valid, amount: 'diez' }).errors.amount, 'invalid');
});

test('mock: valida y responde un número de prueba sin registrar', async () => {
  const res = await createHandler({ mode: 'mock', log: silent, now: () => new Date('2026-11-03T15:00:00Z') })(ev(valid));
  assert.equal(JSON.parse(res.body).number, 'LR-2026-MOCK');
});

test('la constancia incluye los datos exigidos y el plazo de 15 días hábiles', () => {
  const t = claimText({ ...valid, number: 'LR-2026-000001', createdAt: '2026-11-03T15:00:00.000Z' }, { name: 'Pati.pe', ruc: '20616635485', address: 'Los Totorales 163, San Miguel' });
  for (const must of ['LR-2026-000001', 'RUC 20616635485', 'DNI: 45678912', 'Monto reclamado', 'Pedido:', '15 días hábiles', 'Indecopi']) assert.ok(t.includes(must), must);
});
