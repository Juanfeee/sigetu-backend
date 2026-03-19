"""Script para inicializar la BD con migraciones y datos iniciales."""

import sys
from sqlalchemy.orm import Session
from app.db.sesion import engine, SessionLocal
from app.db.datos_iniciales import seed_roles, seed_default_users

def init_database():
    """Ejecuta seeds de datos iniciales."""
    db: Session = SessionLocal()
    try:
        print("▶️ Cargando roles...")
        seed_roles(db)
        print("✅ Roles cargados exitosamente")
        
        print("▶️ Cargando usuarios de prueba...")
        seed_default_users(db)
        print("✅ Usuarios cargados exitosamente")
        
        print("✅ Base de datos inicializada correctamente")
        return 0
    except Exception as e:
        print(f"❌ Error al inicializar BD: {e}", file=sys.stderr)
        return 1
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(init_database())
