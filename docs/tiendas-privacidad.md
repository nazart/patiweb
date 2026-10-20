# Guía para publicar Pati en las tiendas: privacidad y requisitos

Basada en cómo funciona la app según el equipo de la app (2026-10-20) y en la
política publicada en https://pati.pe/privacidad/. Si la app cambia, actualizar
esta guía, `tools/site/legal.py` y los formularios de las tiendas a la vez.

## URLs para las fichas

| Campo | URL |
|---|---|
| Política de privacidad (Google Play y App Store) | https://pati.pe/privacidad/ |
| Términos (pantalla de login de la app) | https://pati.pe/terminos/ |
| Eliminación de cuenta (Google Play → Data safety) | https://pati.pe/eliminar-cuenta/ |
| Soporte / contacto | https://pati.pe/contacto/ · hola@pati.pe |

## Pendientes en la app antes de enviar (bloqueantes)

1. **Eliminar cuenta dentro de la app** en *Perfil → Eliminar cuenta* (la web describe esa ruta). Debe borrar
   cuenta, perfil, catálogo, fotos, ofertas, créditos, solicitudes con su ubicación y token push dentro de 30 días.
   Aplica también a quienes se registraron por el asistente de WhatsApp. Apple 5.1.1(v) y Google Play la exigen.
2. **Ocultar la compra de créditos** (Culqi/Yape) y cualquier precio de paquetes en las versiones de tienda.
   Vender créditos dentro de la app con un pago externo infringe Apple 3.1.1 y la política de pagos de Google Play.
   Los términos dicen que en el lanzamiento no se venden créditos.
3. **Enlaces del login** “Términos” y “Política de Privacidad” → las URLs de arriba.
4. **Consentimiento de promociones**: casilla opcional, desmarcada por defecto, separada de aceptar los términos;
   guardar fecha y poder retirarlo.
5. **Retención** (lo declarado en la política): solicitudes y su ubicación 12 meses; cuentas eliminadas 30 días;
   conversación del bot 24 h; ajustar la retención de PostHog.
6. Verificar que **Gemini** se use con la API de pago (los datos no se usan para entrenar modelos) y que
   **Sentry** quede sin datos personales al mergearlo.

## Google Play → Data safety

- ¿Recopila o comparte datos? **Sí recopila.** Compartir: **No** (los proveedores que tratan datos por encargo no cuentan como “compartir”).
- ¿Datos cifrados en tránsito? **Sí.** ¿Los usuarios pueden pedir la eliminación? **Sí** → https://pati.pe/eliminar-cuenta/

| Categoría Google | Tipo | Finalidad | Obligatorio |
|---|---|---|---|
| Ubicación | Precisa y aproximada | Funcionalidad de la app | Sí |
| Información personal | Nombre | Funcionalidad, gestión de la cuenta (+ marketing si acepta promociones) | Sí |
| Información personal | Número de teléfono | Gestión de la cuenta, funcionalidad | Sí |
| Información personal | Dirección (negocio del vendedor) | Funcionalidad | Sí (vendedores) |
| Información personal | Otra información (distrito, fecha de nacimiento, género, RUC) | Funcionalidad, gestión de la cuenta | Sí |
| Fotos y videos | Fotos | Funcionalidad | No |
| Mensajes | Otros mensajes (asistente de WhatsApp) | Funcionalidad | No |
| Actividad en la app | Interacciones con la app | Analítica | Sí |
| Actividad en la app | Otro contenido generado (solicitudes, ofertas, calificaciones, denuncias) | Funcionalidad, prevención de fraude | Sí |
| Información y rendimiento | Registros de fallos y diagnósticos (Sentry) | Analítica | Sí |
| Dispositivo u otros ID | Token de notificaciones | Funcionalidad | Sí |

No declarar: información financiera (no hay compras en el lanzamiento), contactos, audio, archivos, ID de publicidad.

## App Store → App Privacy

- **Tracking: No.** No hay SDK de publicidad ni se usa el IDFA.

| Tipo Apple | Vinculado al usuario | Finalidad |
|---|---|---|
| Contact Info → Name | Sí | App Functionality (+ Developer’s Marketing si acepta promociones) |
| Contact Info → Phone Number | Sí | App Functionality |
| Contact Info → Physical Address (vendedores) | Sí | App Functionality |
| Location → Precise Location y Coarse Location | Sí | App Functionality |
| User Content → Photos or Videos | Sí | App Functionality |
| User Content → Other User Content (solicitudes, ofertas, calificaciones, denuncias) | Sí | App Functionality |
| Identifiers → User ID (ID interno en PostHog) | Sí | Analytics, App Functionality |
| Usage Data → Product Interaction | Sí | Analytics |
| Diagnostics → Crash Data y Performance Data | No | App Functionality |
| Other Data → Other Data Types (fecha de nacimiento, género, distrito, RUC) | Sí | App Functionality |

## Riesgos que conviene revisar con un abogado cuando sea posible

1. Inscripción del banco de datos en el RNPDP (la política lo declara “en trámite”) y si aplica designar oficial de datos personales según el reglamento vigente de la Ley 29733.
2. Consentimiento para la transferencia internacional a EE. UU. y para promociones (cómo se recoge y registra en la app).
3. Cláusula de responsabilidad de los Términos frente al Código de Protección y Defensa del Consumidor.
4. Comprobantes de pago (SUNAT) cuando se habilite la venta de créditos.
