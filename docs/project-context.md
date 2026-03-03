# Contexto del proyecto: SIGETU Backend

## Resumen funcional
SIGETU Backend soporta la gestión de citas para atención estudiantil. Un estudiante agenda su cita y una secretaría administra la cola de atención hasta finalizar el caso.

## Problema que resuelve
Centraliza la asignación y seguimiento de citas para evitar desorden en atención académica/administrativa y dar trazabilidad del estado de cada solicitud.

## Roles y capacidades
- Estudiante:
  - Inicia sesión.
  - Crea cita con categoría, contexto y fecha/hora programada (`scheduled_at`).
  - Consulta sus citas actuales e historial.
  - Edita/cancela su cita si está en estado `pendiente`.
- Secretaría:
  - Consulta cola filtrada por su `programa_academico`.
  - Cambia estado de citas según transiciones permitidas.
  - Consulta detalle e historial de atención.

## Flujo principal de citas
1. Estudiante autenticado crea cita.
2. Cita entra como `pendiente`.
3. Secretaría avanza estado (`llamando` → `en_atencion` → final).
4. Estados finales (`atendido`, `no_asistio`, `cancelada`) se archivan en historial.

## Reglas de negocio vigentes
- Categorías válidas: `academico`, `administrativo`, `financiero`, `otro`.
- Estados válidos: `pendiente`, `llamando`, `en_atencion`, `atendido`, `no_asistio`, `cancelada`.
- No se permite agendar en fecha/hora pasada.
- Una secretaría solo opera sobre estudiantes de su mismo `programa_academico`.

## Contexto técnico
- FastAPI para API REST y rutas WebSocket.
- SQLAlchemy para persistencia.
- Alembic para versionado de esquema.
- Seed en startup para roles/usuarios por defecto.

## Endpoints clave (alto nivel)
- Autenticación: `/auth/*`
- Citas estudiante: `/appointments`, `/appointments/me`, `/appointments/{id}`, `/appointments/{id}/cancel`
- Gestión secretaría/cola: rutas en módulo de secretaría y actualización de estado.

## Decisiones de diseño actuales
- Separación por capas (routes/services/repositories).
- Validaciones de negocio centralizadas en servicios.
- Modelos y constraints de BD alineados con estados/categorías permitidos.

## Alcance actual (MVP)
- Gestión básica de ciclo de vida de citas.
- Historial de citas finalizadas.
- Eventos en tiempo real para cambios de citas.

## Pendientes potenciales
- Pruebas automatizadas de flujos críticos.
- Documentación de contratos por rol y ejemplos de payloads.
- Definir políticas de zona horaria de extremo a extremo (cliente/API/BD).

## Cómo mantener este documento
Actualizar este archivo cuando cambie:
- una regla de negocio,
- el flujo de estados,
- contratos principales de API,
- o decisiones arquitectónicas relevantes.
