# Instrucciones del proyecto SIGETU Backend

## Objetivo
Backend para gestión de citas académicas con dos roles principales:
- Estudiante: crea, consulta, edita y cancela sus citas.
- Secretaría: gestiona la cola y actualiza estados de atención.

## Stack y arquitectura
- Framework: FastAPI
- ORM: SQLAlchemy
- Migraciones: Alembic
- Base de datos: PostgreSQL
- Estructura por capas:
  - `app/api/routes`: endpoints HTTP/WS
  - `app/services`: reglas de negocio
  - `app/repositories`: acceso a datos
  - `app/models`: entidades ORM
  - `app/schemas`: contratos de entrada/salida

## Convenciones de código
- Mantener cambios mínimos y enfocados al requerimiento.
- Evitar lógica de negocio en rutas; ubicarla en `services`.
- Evitar acceso directo a DB desde rutas; usar `repositories` vía `services`.
- Reutilizar esquemas Pydantic existentes antes de crear nuevos.
- No introducir dependencias nuevas sin necesidad clara.
- No renombrar endpoints o contratos públicos salvo que se solicite explícitamente.

## Reglas de negocio clave
- Estados de cita válidos: `pendiente`, `llamando`, `en_atencion`, `atendido`, `no_asistio`, `cancelada`.
- Transiciones de estado deben respetar el flujo definido en `AppointmentService`.
- `scheduled_at` no puede quedar en fecha/hora pasada.
- La secretaría solo puede ver/gestionar citas de su `programa_academico`.

## API y seguridad
- Autenticación por JWT.
- Validación de permisos por rol en dependencias de autenticación.
- Errores de negocio con `HTTPException` y mensajes claros en español.
- Mantener consistencia de códigos HTTP existentes.

## Base de datos y migraciones
- Toda modificación de modelos debe acompañarse con migración Alembic.
- No borrar ni reescribir migraciones históricas ya aplicadas.
- Mantener constraints/checks alineados con enums lógicos de negocio.

## Calidad y validación
- Verificar que los cambios no rompan rutas existentes.
- Cuando aplique, validar con pruebas manuales mínimas (login, crear cita, cambio de estado).
- No corregir bugs no relacionados, salvo que bloqueen el requerimiento actual.

## Qué evitar
- No hardcodear credenciales ni secretos.
- No agregar comentarios innecesarios o código muerto.
- No mezclar refactors grandes con un cambio funcional pequeño.

## Checklist antes de cerrar cambios
- ¿El cambio cumple exactamente el requerimiento?
- ¿La lógica de negocio quedó en `services`?
- ¿La API mantiene contratos esperados?
- ¿Hay migración si cambió modelo?
- ¿Se validó el flujo principal afectado?
