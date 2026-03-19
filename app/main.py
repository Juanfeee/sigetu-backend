"""Punto de entrada de FastAPI: registra middlewares, rutas y datos semilla."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.sesion import SessionLocal
from app.api.routes import rutas_ws_citas
from app.api.routes import rutas_autenticacion
from app.api.routes.estudiante import rutas_citas as rutas_citas_estudiante
from app.api.routes.secretaria import rutas_citas as rutas_citas_secretaria


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rutas_autenticacion.router)
app.include_router(rutas_citas_estudiante.router)
app.include_router(rutas_citas_secretaria.router)
app.include_router(rutas_ws_citas.router)
# Nota: seed_roles y seed_default_users se ejecutan vía init_db.py en el Procfile
# No ejecutar aquí porque las tablas aún no existen durante el startup de Alembic