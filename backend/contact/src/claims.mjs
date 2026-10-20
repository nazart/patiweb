// Libro de Reclamaciones virtual (Ley 29571, art. 150; DS 011-2011-PCM y modificatorias).
// Valida la Hoja de Reclamación y arma el texto de la constancia que recibe el consumidor.

export const DOC_TYPES = ['DNI', 'CE', 'Pasaporte'];
export const CLAIM_TYPES = ['reclamo', 'queja'];
export const ITEM_TYPES = ['producto', 'servicio'];

const LIM = { name: 120, doc: 12, address: 200, phone: 20, email: 160, desc: 1000, detail: 3000, request: 1500 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const DOC_RE = { DNI: /^\d{8}$/, CE: /^[A-Za-z0-9]{9,12}$/, Pasaporte: /^[A-Za-z0-9]{6,12}$/ };
const clean = (v, max) => (typeof v === 'string' ? v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max) : '');

export function validateClaim(body) {
  if (!body || typeof body !== 'object') return { ok: false, errors: { body: 'invalid' } };
  if (typeof body.website === 'string' && body.website.trim() !== '') return { ok: false, bot: true, errors: {} };

  const d = {
    name: clean(body.name, LIM.name),
    docType: clean(body.docType, 10),
    docNumber: clean(body.docNumber, LIM.doc).toUpperCase(),
    address: clean(body.address, LIM.address),
    phone: clean(body.phone, LIM.phone),
    email: clean(body.email, LIM.email).toLowerCase(),
    isMinor: body.isMinor === true || body.isMinor === 'true',
    guardianName: clean(body.guardianName, LIM.name),
    guardianDoc: clean(body.guardianDoc, LIM.doc).toUpperCase(),
    itemType: clean(body.itemType, 10),
    amount: clean(String(body.amount ?? ''), 12),
    itemDescription: clean(body.itemDescription, LIM.desc),
    claimType: clean(body.claimType, 10),
    detail: clean(body.detail, LIM.detail),
    request: clean(body.request, LIM.request),
  };

  const e = {};
  if (d.name.length < 3) e.name = 'required';
  if (!DOC_TYPES.includes(d.docType)) e.docType = 'invalid';
  else if (!DOC_RE[d.docType].test(d.docNumber)) e.docNumber = 'invalid';
  if (d.address.length < 5) e.address = 'required';
  if (!/^[+\d\s()-]{6,20}$/.test(d.phone)) e.phone = 'invalid';
  if (!EMAIL_RE.test(d.email)) e.email = 'invalid';
  if (d.isMinor) {
    if (d.guardianName.length < 3) e.guardianName = 'required';
    if (!/^[A-Z0-9]{6,12}$/.test(d.guardianDoc)) e.guardianDoc = 'invalid';
  }
  if (!ITEM_TYPES.includes(d.itemType)) e.itemType = 'invalid';
  if (d.amount && !/^\d{1,9}(\.\d{1,2})?$/.test(d.amount)) e.amount = 'invalid';
  if (d.itemDescription.length < 3) e.itemDescription = 'required';
  if (!CLAIM_TYPES.includes(d.claimType)) e.claimType = 'invalid';
  if (d.detail.length < 10) e.detail = 'required';
  if (d.request.length < 5) e.request = 'required';
  if (body.accept !== true && body.accept !== 'true') e.accept = 'required';

  return Object.keys(e).length ? { ok: false, errors: e } : { ok: true, data: d };
}

// Texto de la Hoja de Reclamación (constancia para el consumidor y aviso para Pati).
export function claimText(c, provider) {
  return [
    `HOJA DE RECLAMACIÓN N.º ${c.number}`,
    `Fecha: ${c.createdAt}`,
    '',
    `Proveedor: ${provider.name} · RUC ${provider.ruc} · ${provider.address}`,
    '',
    '1. Consumidor reclamante',
    `Nombre: ${c.name}`,
    `${c.docType}: ${c.docNumber}`,
    `Domicilio: ${c.address}`,
    `Teléfono: ${c.phone} · Correo: ${c.email}`,
    ...(c.isMinor ? [`Menor de edad. Padre, madre o apoderado: ${c.guardianName} (doc. ${c.guardianDoc})`] : []),
    '',
    '2. Identificación del bien contratado',
    `Tipo: ${c.itemType} · Monto reclamado: ${c.amount ? 'S/ ' + c.amount : 'no indicado'}`,
    `Descripción: ${c.itemDescription}`,
    '',
    "3. Detalle de la reclamación y pedido del consumidor",
    `Tipo: ${c.claimType === 'reclamo' ? 'Reclamo (disconformidad con el producto o servicio)' : 'Queja (disconformidad con la atención)'}`,
    `Detalle: ${c.detail}`,
    `Pedido: ${c.request}`,
    '',
    'Pati dará respuesta en un plazo no mayor a 15 días hábiles improrrogables.',
    'La formulación del reclamo no impide acudir a otras vías de solución de controversias ni es requisito previo para interponer una denuncia ante el Indecopi.',
  ].join('\n');
}
