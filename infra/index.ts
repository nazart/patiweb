// Infraestructura del formulario de contacto de pati.pe.
// Web (Amplify, ya existente) → POST https://<api>/contact → Lambda → DynamoDB + SES + Google Sheets.
import * as path from "path";
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const cfg = new pulumi.Config();
const mode = cfg.get("mode") ?? "mock";
const domain = cfg.require("domain");
const mailFrom = cfg.require("mailFrom");
const mailTo = cfg.require("mailTo");
const allowedOrigins = cfg.requireObject<string[]>("allowedOrigins");
const sheetId = cfg.get("sheetId") ?? "";
const name = "pati-contact";
const tags = { project: "pati", component: "contact" };

// --- Datos: una sola tabla para mensajes (pk "msg#…") y contadores del límite por IP (pk "rl#…", con TTL).
const table = new aws.dynamodb.Table(name, {
    name,
    billingMode: "PAY_PER_REQUEST",
    hashKey: "pk",
    attributes: [{ name: "pk", type: "S" }],
    ttl: { attributeName: "expiresAt", enabled: true },
    pointInTimeRecovery: { enabled: true },
    tags,
});

// --- Correo: dominio verificado en SES con DKIM publicado en Route 53.
const zone = aws.route53.getZoneOutput({ name: domain });
const identity = new aws.sesv2.EmailIdentity(`${name}-domain`, { emailIdentity: domain, tags });
const dkimRecords = [0, 1, 2].map((i) =>
    new aws.route53.Record(`${name}-dkim-${i}`, {
        zoneId: zone.zoneId,
        name: identity.dkimSigningAttributes.apply((a) => `${a.tokens![i]}._domainkey.${domain}`),
        type: "CNAME",
        ttl: 1800,
        records: [identity.dkimSigningAttributes.apply((a) => `${a.tokens![i]}.dkim.amazonses.com`)],
    }),
);

// --- Credencial de la cuenta de servicio de Google. El valor (JSON) se carga fuera de Pulumi:
//     aws secretsmanager put-secret-value --secret-id pati-contact/google-sa --secret-string file://sa.json
const googleSecret = new aws.secretsmanager.Secret(`${name}-google-sa`, { name: `${name}/google-sa`, tags });

// --- Lambda
const logGroup = new aws.cloudwatch.LogGroup(`${name}-logs`, { name: `/aws/lambda/${name}`, retentionInDays: 30, tags });

const role = new aws.iam.Role(`${name}-role`, {
    assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({ Service: "lambda.amazonaws.com" }),
    tags,
});
new aws.iam.RolePolicy(`${name}-policy`, {
    role: role.id,
    policy: pulumi.jsonStringify({
        Version: "2012-10-17",
        Statement: [
            { Effect: "Allow", Action: ["logs:CreateLogStream", "logs:PutLogEvents"], Resource: pulumi.interpolate`${logGroup.arn}:*` },
            { Effect: "Allow", Action: ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource: table.arn },
            { Effect: "Allow", Action: ["ses:SendEmail"], Resource: identity.arn },
            { Effect: "Allow", Action: ["secretsmanager:GetSecretValue"], Resource: googleSecret.arn },
        ],
    }),
});

const fn = new aws.lambda.Function(name, {
    name,
    runtime: aws.lambda.Runtime.NodeJS22dX,
    architectures: ["arm64"],
    handler: "handler.handler",
    code: new pulumi.asset.FileArchive(path.join(__dirname, "..", "backend", "contact", "src")),
    role: role.arn,
    memorySize: 256,
    timeout: 10,
    environment: {
        variables: {
            MODE: mode,
            TABLE_NAME: table.name,
            MAIL_FROM: mailFrom,
            MAIL_TO: mailTo,
            GOOGLE_SECRET_ARN: googleSecret.arn,
            SHEET_ID: sheetId,
            SHEET_TAB: "Mensajes",
            RATE_LIMIT_PER_HOUR: "5",
            // Datos del proveedor para la Hoja de Reclamación.
            PROVIDER_NAME: "Pati.pe",
            PROVIDER_RUC: "20616635485",
            PROVIDER_ADDRESS: "Los Totorales 163, San Miguel",
        },
    },
    tags,
}, { dependsOn: [logGroup] });

// --- API pública: HTTP API con CORS solo para los dominios de la web y throttling.
const api = new aws.apigatewayv2.Api(`${name}-api`, {
    name: `${name}-api`,
    protocolType: "HTTP",
    corsConfiguration: {
        allowOrigins: allowedOrigins,
        allowMethods: ["POST", "OPTIONS"],
        allowHeaders: ["content-type"],
        maxAge: 86400,
    },
    tags,
});
const integration = new aws.apigatewayv2.Integration(`${name}-integration`, {
    apiId: api.id,
    integrationType: "AWS_PROXY",
    integrationUri: fn.invokeArn,
    payloadFormatVersion: "2.0",
});
new aws.apigatewayv2.Route(`${name}-route`, {
    apiId: api.id,
    routeKey: "POST /contact",
    target: pulumi.interpolate`integrations/${integration.id}`,
});
// Libro de Reclamaciones virtual: correlativo, registro y copia por correo al consumidor.
// Nota: para enviar la copia a cualquier correo, SES debe salir del sandbox (solicitud de acceso de producción).
new aws.apigatewayv2.Route(`${name}-claims-route`, {
    apiId: api.id,
    routeKey: "POST /reclamos",
    target: pulumi.interpolate`integrations/${integration.id}`,
});
new aws.apigatewayv2.Stage(`${name}-stage`, {
    apiId: api.id,
    name: "$default",
    autoDeploy: true,
    defaultRouteSettings: { throttlingBurstLimit: 10, throttlingRateLimit: 5 },
    tags,
});
new aws.lambda.Permission(`${name}-invoke`, {
    action: "lambda:InvokeFunction",
    function: fn.name,
    principal: "apigateway.amazonaws.com",
    sourceArn: pulumi.interpolate`${api.executionArn}/*/*`,
});

export const contactEndpoint = pulumi.interpolate`${api.apiEndpoint}/contact`;
export const claimsEndpoint = pulumi.interpolate`${api.apiEndpoint}/reclamos`;
export const tableName = table.name;
export const googleSecretName = googleSecret.name;
export const lambdaMode = mode;
export const dkimRecordNames = dkimRecords.map((r) => r.name);
