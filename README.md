# SIGETU Backend

Backend de gestión de citas construido con FastAPI + SQLAlchemy + Alembic.

## Requisitos

- Python 3.11+ (recomendado 3.12/3.13)
- PostgreSQL activo
- Windows PowerShell (comandos de ejemplo)

## 1) Clonar e instalar dependencias

```powershell
# desde la raíz del proyecto
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2) Configurar variables de entorno

Crea/edita el archivo `.env` en la raíz:

```env
DATABASE_URL=postgresql://postgres:12345678@localhost:5432/sigetu
SECRET_KEY=tu_secret_key_larga
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 3) Ejecutar migraciones

Usa siempre Alembic con el Python del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m alembic current
```

## 4) Levantar el servidor

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Documentación interactiva:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 5) Usuarios semilla (se crean en startup)

Contraseña por defecto:

- `12345678`

Ejemplos útiles:

- Estudiante: `estudiante.ingenierias@uniautonoma.edu.co`
- Secretaría: `secretaria.ingenierias@uniautonoma.edu.co`
- Secretaría general: `secretaria@uniautonoma.edu.co`

## Flujo rápido de prueba

1. Login estudiante en `/auth/login`
2. Crear cita en `POST /appointments`
3. Login secretaría en `/auth/login`
4. Cambiar estado en `PATCH /appointments/{appointment_id}/status`

Body para cambio de estado:

```json
{
  "status": "llamando"
}
```

## Solución de problemas

### `alembic` no se reconoce en terminal

Ejecuta con:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

### Error de bcrypt/passlib al iniciar

Este proyecto fija `bcrypt==3.2.2` para compatibilidad con `passlib==1.7.4`.
Si ya tenías otra versión instalada, reinstala:

```powershell
python -m pip install -r requirements.txt
```
