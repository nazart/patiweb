// Validación y normalización del cuerpo que envía el formulario de /contacto/.

export const REASONS = [
  'Uso de la app', 'Idea o sugerencia', 'Quiero vender en Pati',
  'Prensa', 'Alianzas', 'Inversión', 'Otro',
];

const LIMITS = { name: 120, email: 160, phone: 20, message: 2000 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const clean = (v, max) => (typeof v === 'string' ? v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max) : '');

// Devuelve { ok: true, data } o { ok: false, errors: { campo: motivo } }.
// Si el honeypot "website" viene lleno, marca bot: true para descartarlo en silencio.
export function validate(body) {
  if (!body || typeof body !== 'object') return { ok: false, errors: { body: 'invalid' } };
  if (typeof body.website === 'string' && body.website.trim() !== '') return { ok: false, bot: true, errors: {} };

  const data = {
    name: clean(body.name, LIMITS.name),
    email: clean(body.email, LIMITS.email).toLowerCase(),
    phone: clean(body.phone, LIMITS.phone),
    reason: clean(body.reason, 40),
    message: clean(body.message, LIMITS.message),
    page: clean(body.page, 120) || '/contacto/',
  };

  const errors = {};
  if (data.name.length < 2) errors.name = 'required';
  if (!EMAIL_RE.test(data.email)) errors.email = 'invalid';
  if (data.phone && !/^[+\d\s()-]{6,20}$/.test(data.phone)) errors.phone = 'invalid';
  if (!REASONS.includes(data.reason)) errors.reason = 'invalid';
  if (data.message.length < 5) errors.message = 'required';

  return Object.keys(errors).length ? { ok: false, errors } : { ok: true, data };
}
