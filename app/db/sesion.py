"""Configuración de engine y sesiones de base de datos para FastAPI."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.configuracion import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def obtener_db():
    """Entrega una sesión transaccional por request y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()