# Requerimientos para la app Pati antes de publicar en tiendas

**Para:** equipo de la app (sesión `pati-04`) · **De:** web pati.pe · **Fecha:** 20 de octubre de 2026 (REQ-10 y REQ-11 añadidos el 22 de octubre)
**Contexto:** la Política de privacidad, los Términos y la página de eliminación de cuenta de pati.pe
describen cómo funciona la app (según lo informado por el equipo de la app el 2026-10-20). Para que la app
sea aprobada por Google Play y App Store, y para que lo publicado sea cierto, la app debe cumplir lo
siguiente. Prioridad **P0 = bloquea el envío a tiendas**.

Referencias: https://pati.pe/privacidad/ · https://pati.pe/terminos/ · https://pati.pe/eliminar-cuenta/ ·
https://pati.pe/libro-de-reclamaciones/ · guía de formularios: `docs/tiendas-privacidad.md`.

---

## REQ-01 · Eliminar cuenta dentro de la app — P0

**Por qué:** Apple (guía 5.1.1(v)) y Google Play exigen poder eliminar la cuenta desde la app. Google además
exige una URL web (ya existe: pati.pe/eliminar-cuenta). La web dice: *Perfil → Eliminar cuenta*.

**Criterios de aceptación**
- [ ] En **Perfil** hay una opción **“Eliminar cuenta”** (comprador y vendedor).
- [ ] Pantalla de confirmación que explica qué se borra y que se pierden los créditos; requiere confirmación explícita (p. ej., escribir “ELIMINAR” o volver a verificar el OTP).
- [ ] Al confirmar: se cierra la sesión y la cuenta queda inaccesible de inmediato.
- [ ] Dentro de **30 días** se eliminan: cuenta y perfil (nombre, celular, distrito, fecha de nacimiento, género), perfil de negocio, catálogo, fotos en S3, ofertas, créditos, solicitudes con su latitud/longitud, token push, y el usuario en PostHog.
- [ ] Se conservan, solo para ese fin y con estos plazos (publicados en pati.pe/eliminar-cuenta):
  - registros de compras de créditos (`Payment`): 5 años;
  - hojas del Libro de Reclamaciones: al menos 2 años;
  - denuncias y sanciones por fraude o abuso (`SellerReport`, `isBanned`): mientras dure el caso, hasta 2 años;
  - calificaciones (`SellerRating`) que dejó el usuario: se **anonimizan** (sin `buyerId` ni nombre), se mantienen en el perfil del vendedor;
  - logs: se borran solos a los 30 días (REQ-12).
- [ ] También se eliminan: `Feedback`, `Notification`, `Favorite`, `PushToken`, `SellerReferralCode` y la persona en PostHog.
- [ ] Funciona también para usuarios registrados solo por el asistente de WhatsApp (vía solicitud manual de soporte).
- [ ] Endpoint de backoffice para atender solicitudes que lleguen por WhatsApp/correo (hola@pati.pe).

## REQ-02 · Ocultar la compra de créditos en las versiones de tienda — P0

**Por qué:** vender créditos (bien digital) con un pago externo (Culqi/Yape) dentro de la app infringe Apple 3.1.1
y la política de pagos de Google Play. Los Términos dicen que **en el lanzamiento no se venden créditos**.

- [ ] No aparecen pantallas, botones, precios ni paquetes de compra de créditos (S/ 10, 20, 30) en la app.
- [ ] No hay enlaces que lleven a comprar créditos fuera de la app.
- [ ] Se mantienen: 20 de bienvenida (una vez), 15 cada mes calendario (no acumulables), referidos 10 + 10.
- [ ] Mensaje cuando el vendedor se queda sin créditos: “Recibirás 15 créditos gratis el próximo mes. También puedes invitar a otro negocio con tu código.”
- [ ] Feature flag (`CREDITS_PURCHASE_ENABLED=false`) para habilitarlo en el futuro tras decidir el medio de pago.
- [ ] En producción, deshabilitar también los endpoints de compra: `payment-service` (cargo Culqi/Yape) y la compra simulada de `credits-service/src/credits/credits.controller.ts`.

## REQ-03 · Enlaces legales en la app — P0

- [ ] El texto del login “Al continuar aceptas nuestros Términos y Política de Privacidad” enlaza a https://pati.pe/terminos/ y https://pati.pe/privacidad/ (navegador in-app).
- [ ] En **Perfil → Ayuda / Legal**: Términos, Privacidad, **Libro de Reclamaciones** (https://pati.pe/libro-de-reclamaciones/), Eliminar cuenta y Contacto (https://pati.pe/contacto/).
- [ ] Se registra la fecha y la versión de los Términos aceptados por cada usuario (`terms_version = "2026-10-31"`).

## REQ-04 · Consentimiento opcional para promociones — P1

**Por qué:** la política declara las promociones como finalidad opcional (Ley 29733).

- [ ] En el registro, casilla **desmarcada por defecto**, separada de aceptar los Términos: “Quiero recibir novedades y promociones de Pati.”
- [ ] Se guarda `marketing_consent` (true/false) con fecha y hora.
- [ ] Se puede retirar desde **Perfil → Notificaciones**.
- [ ] Ninguna campaña promocional (push, SMS, WhatsApp) se envía a quien no aceptó.

## REQ-05 · Plazos de conservación declarados — P1

- [ ] Job programado que elimina o anonimiza **solicitudes y su latitud/longitud con más de 12 meses**.
- [ ] Job que completa la eliminación de cuentas a los **30 días** (REQ-01).
- [ ] Estado del asistente de WhatsApp: se mantiene en **24 horas** (ya es así).
- [ ] Retención de eventos en PostHog configurada en **12 meses** como máximo.

## REQ-06 · Proveedores y datos — P1

- [ ] **Gemini:** usar la API de pago (los datos no se usan para entrenar modelos) y no enviar el número de celular ni el nombre del comprador; solo texto de solicitudes/productos.
- [ ] **Sentry:** al mergear, mantener `sendDefaultPii: false`, sin capturas ni cuerpos de peticiones.
- [ ] **PostHog:** identificar solo con el ID interno (ya es así); no enviar teléfono, nombre ni ubicación precisa como propiedades.
- [ ] Confirmar que el vendedor **no** recibe el teléfono del comprador en ninguna respuesta de la API.
- [ ] **LLM de relevancia** (`matching-service/src/matching/relevance.service.ts`): usa `RELEVANCE_PROVIDER=jev` (TypeSafe AI, EE. UU.), ya declarado en la política (22 oct). Enviar solo el texto de la solicitud y el nombre y la descripción de los productos: nunca el teléfono, el nombre ni la ubicación. Declararlo también en Data safety y App Privacy.
- [ ] **ngrok:** solo en desarrollo. Que no esté activo en producción (sin `NGROK_AUTHTOKEN`).
- [ ] Si se agrega un proveedor nuevo, avisar para actualizar la política y los formularios de las tiendas.

## REQ-07 · Permisos del sistema — P1

- [ ] Ubicación solo **“mientras se usa la app”** (sin `ACCESS_BACKGROUND_LOCATION` ni “Siempre” en iOS).
- [ ] Textos de permiso en iOS (`Info.plist`), en español:
  - `NSLocationWhenInUseUsageDescription`: “Pati usa tu ubicación para encontrar vendedores cerca de ti y mostrarte cómo llegar.”
  - `NSPhotoLibraryUsageDescription`: “Pati usa tus fotos solo para adjuntarlas a tus pedidos, ofertas y productos.” (hoy no está en `app.json`: configurarlo en el plugin `expo-image-picker` con `photosPermission` y `cameraPermission: false`).
- [ ] Revisar el manifest final del APK/AAB de EAS: que `expo-image-picker` no agregue `CAMERA` ni `RECORD_AUDIO`.
- [ ] Si no hay uso de cámara, no declarar `NSCameraUsageDescription` ni el permiso `CAMERA` en Android.
- [ ] Sin SDK de publicidad ni IDFA: en iOS no mostrar ATT; en Google Play declarar “no usa ID de publicidad”.

## REQ-12 · Logs sin datos personales y con plazo — P1

**Por qué:** la política declara que los registros técnicos del servidor se guardan **30 días**. Hoy varios servicios
registran el teléfono, el texto de WhatsApp y la ubicación en texto plano, y los logs de pm2 en la EC2 no tienen
retención.

- [ ] Enmascarar el teléfono en los logs (`+51 9•• ••• 233`) y no registrar el texto ni la ubicación de los mensajes de WhatsApp: `whatsapp-service` (`webhook.controller.ts:49`, `webhook.service.ts:187/258/271`, `conversation.service.ts:38/45`), `user-service/users.service.ts:425` y `notification-service/notifications.service.ts:261`.
- [ ] El log del OTP (`auth-service/otp.service.ts:53`) solo en modo MOCK; nunca en producción.
- [ ] Rotación de logs de pm2 (`pm2-logrotate`) o CloudWatch con `RetentionInDays: 30`.
- [ ] Retención de PostHog y Sentry configurada en sus paneles (PostHog ≤ 12 meses, Sentry 30–90 días).

## REQ-08 · Edad mínima y soporte — P2

- [ ] Validación de 18 años en el registro (ya existe) con mensaje claro si no cumple.
- [ ] El mensaje de cuenta suspendida incluye cómo contactar: “Escríbenos a hola@pati.pe o por WhatsApp al +51 924 519 233.”

## REQ-09 · Fichas de las tiendas — P0

- [ ] Política de privacidad: https://pati.pe/privacidad/ · Eliminación de cuenta: https://pati.pe/eliminar-cuenta/ · Soporte: https://pati.pe/contacto/ · correo hola@pati.pe.
- [ ] Llenar “Data safety” (Google) y “App Privacy” (Apple) según `docs/tiendas-privacidad.md`.
- [ ] **Antes de enviar a revisión**, esas URLs deben estar publicadas en **pati.pe** (producción), no solo en dev-web.

## REQ-10 · Bloquear usuarios — P0

**Por qué:** Apple (guía 1.2, contenido generado por usuarios) exige poder **denunciar** contenido, **bloquear**
a usuarios abusivos y que el equipo actúe a tiempo. Google Play tiene una exigencia equivalente. Los Términos
(sección “Calificaciones, denuncias y bloqueo”) ya lo describen; por eso debe existir antes del envío.

**Criterios de aceptación**
- [ ] En una oferta y en el perfil de un vendedor hay una opción **“Bloquear”**, con confirmación.
- [ ] El comprador deja de recibir ofertas del vendedor bloqueado.
- [ ] El vendedor bloqueado deja de ver las solicitudes de ese comprador y no puede volver a ofertarle.
- [ ] El vendedor también puede bloquear a un comprador.
- [ ] En **Perfil → Usuarios bloqueados** se ven los bloqueos y se pueden deshacer.
- [ ] Bloquear no le avisa a la otra persona.
- [ ] El bloqueo se aplica también en el asistente de WhatsApp.

## REQ-11 · Denuncias atendidas en 24 horas — P0

**Por qué:** los Términos prometen que **una persona revisa cada denuncia en un máximo de 24 horas** y que
podemos retirar el contenido, advertir, suspender o cerrar la cuenta. Apple pide que el desarrollador actúe
sobre el contenido denunciado de forma oportuna.

**Criterios de aceptación**
- [ ] Cada denuncia nueva notifica al equipo al instante (correo a info@pati.pe y/o un canal interno).
- [ ] El backoffice muestra las denuncias pendientes con su antigüedad y una alerta pasadas 20 horas.
- [ ] Las acciones disponibles son retirar la oferta o el contenido (deja de verse de inmediato), advertir, suspender temporalmente y cerrar la cuenta.
- [ ] Cada acción queda registrada: quién, cuándo y por qué.
- [ ] El denunciante ve en la app que su denuncia fue recibida (“La revisaremos en un máximo de 24 horas”).
- [ ] Al denunciar, la app ofrece también bloquear a ese usuario.

---

### Si algo de esto no coincide con la app
Avisar a la web (repo `patiweb`, `tools/site/legal.py`) para corregir la política o los términos **antes** de
enviar a las tiendas: lo publicado y lo declarado en las fichas deben coincidir con lo que hace la app.
