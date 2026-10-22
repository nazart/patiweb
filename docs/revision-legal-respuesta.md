# Respuesta a la revisión de las páginas legales

**Fecha:** 22 de octubre de 2026 · **Revisión recibida:** “Evaluación de las páginas legales de PaTi” (decisión: REQUIERE CAMBIOS)

La revisión describe una versión anterior y breve de las páginas. La versión publicada el 20 de octubre ya
incluye la mayoría de los puntos. Le pedimos al revisor que evalúe las URLs vigentes, con enlace directo a
cada sección. Si su herramienta muestra una copia en caché, conviene recargar la página o abrirla sin el
parámetro `utm_source`.

- Privacidad: https://dev-web.pati.pe/privacidad/ (en producción: https://pati.pe/privacidad/)
- Términos: https://dev-web.pati.pe/terminos/ (en producción: https://pati.pe/terminos/)
- Eliminación de cuenta: https://dev-web.pati.pe/eliminar-cuenta/

## Política de privacidad

| Observación | Estado | Dónde |
| --- | --- | --- |
| Datos recopilados (ubicación, fotos, notificaciones…) | Cumple | `/privacidad/#datos` (tabla por tipo de dato) y `#permisos` |
| Finalidades | Cumple | `#finalidades`: necesarias y opcionales (promociones con consentimiento); `#automatizado` |
| Terceros y proveedores | Cumple | `#proveedores` (proveedor, dato, finalidad y país) y `#transferencias` (EE. UU.) |
| Medidas de seguridad | Cumple | `#seguridad` |
| Conservación | Cumple | `#conservacion` (plazo por tipo de dato) |
| Eliminación de cuenta y datos | Cumple en la web; la app lo implementa (REQ-01) | `#eliminar` y `/eliminar-cuenta/` |
| Contacto de privacidad | Cumple | `#responsable` y `#derechos` (ARCO, ANPD) |
| Pagos | Cumple (22 oct) | `#datos` y `#proveedores`: número de Yape y datos de la compra con Culqi, solo cuando se habilite; sin tarjetas |

## Términos y condiciones

| Observación | Estado | Dónde |
| --- | --- | --- |
| Reglas para publicar contenido | Cumple | `/terminos/#requisitos`, `#reglas` y `#contenido` |
| Contenido prohibido y abuso | Cumple | `#reglas` (“Lo que no está permitido”) |
| Denuncias y moderación | Cumple (22 oct) | `#calificaciones`: denunciar, **bloquear**, revisión humana en un máximo de **24 horas** y medidas (retirar, advertir, suspender, cerrar) |
| Edad mínima | Cumple: **18 años**, confirmado por la empresa | `#requisitos` y `/privacidad/#menores` |
| Créditos y compras | Cumple | `#creditos`: “Durante el lanzamiento Pati no vende créditos”. La frase sobre comprar créditos en la app ya no existe |

## Pendientes reales (fuera del texto)

| Pendiente | Responsable | Referencia |
| --- | --- | --- |
| Eliminar la cuenta desde la app | App | `docs/requerimientos-app-pati.md` REQ-01 |
| Ocultar la compra de créditos en la versión de tienda | App | REQ-02 |
| Enlaces a privacidad, términos y eliminación dentro de la app | App | REQ-03 |
| Bloquear usuarios | App | REQ-10 |
| Denuncias atendidas en un máximo de 24 horas (backoffice y alertas) | App y operación | REQ-11 |
| Inventario de datos contrastado con el código | App y web | sección siguiente |
| Publicar en producción (pati.pe) antes de enviar a revisión | Web | paso de `staging` a `main` |

## Inventario de datos (22 oct, basado en el código de la app)

El equipo de la app (`pati-04`) entregó el inventario de los esquemas Prisma, los SDK, `app.json`, los logs, los pagos y la moderación.
Resultado del contraste con la política:

| Hallazgo | Acción |
| --- | --- |
| Feedback dentro de la app (ideas, fallas, soporte) no estaba declarado | Agregado a `#datos` |
| Historial de notificaciones (título y texto) | Agregado a `#datos` |
| Ubicación compartida por WhatsApp | Agregada a `#datos` |
| **Pagos:** existe la tabla `Payment` (número de Yape, IDs de Culqi, monto). No hay tarjetas ni se guarda el OTP | Declarado en `#datos` y `#proveedores`, “cuando se habilite”. La app desactiva la compra en producción (REQ-02) |
| Sentry recibe modelo y sistema del dispositivo | Texto corregido: “sin tu nombre ni celular” (antes decía “sin datos personales”) |
| La política decía “no recogemos tu DNI”, pero el Libro de Reclamaciones sí lo pide | Aclarado: “**en la app** no recogemos…” |
| **Logs con teléfono, texto de WhatsApp y ubicación en texto plano, sin retención** | La política declara logs por 30 días; la app los enmascara y les pone retención (REQ-12) |
| **LLM de relevancia typesafe.ai (`RELEVANCE_PROVIDER=jev`) no declarado** | Declarado (decisión de la empresa, 22 oct) en `#proveedores` y `#automatizado`. TypeSafe AI, San Francisco, EE. UU. |
| Bloqueo entre usuarios no existe; las denuncias no avisan a nadie | REQ-10 y REQ-11 (P0) |
| No existen DNI, correo, IP ni device id de usuarios; la ubicación es solo en primer plano; no se usa cámara | Coincide con la política |
