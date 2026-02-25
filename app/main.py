from app.db.seed import seed_roles
from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.api.routes import auth_routes


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    translated_errors = []

    for error in exc.errors():
        raw_loc = error.get("loc", [])
        loc = [str(item) for item in raw_loc if item != "body"]
        field = ".".join(loc) if loc else "request"
        error_type = error.get("type", "")
        original_msg = error.get("msg", "Valor inválido")

        if error_type in {"value_error.missing", "missing"}:
            msg = f"Falta el campo: {field}"
        elif field.endswith("password") and error_type in {"string_too_short", "too_short", "value_error.any_str.min_length"}:
            msg = "La contraseña debe tener al menos 8 caracteres"
        else:
            msg = original_msg

        translated_errors.append(
            {
                "field": field,
                "message": msg,
                "type": error_type,
            }
        )

    return JSONResponse(status_code=422, content={"detail": translated_errors})


app.include_router(auth_routes.router)
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_roles(db)
    db.close()