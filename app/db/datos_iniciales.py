"""Semillas de roles y usuarios base para entornos de desarrollo."""

from sqlalchemy.orm import Session
from app.models.modelo_rol import Role
from app.models.modelo_usuario import User
from app.core.seguridad import hashear_contrasena


SEED_PASSWORD = "12345678"
PROGRAMAS_ACADEMICOS = ["ingenierias", "derecho", "finanzas"]

def seed_roles(db: Session):
    """Crea los roles mínimos requeridos por el flujo de autenticación y sedes."""
    roles = ["admin", "estudiante", "secretaria", "administrativo", "admisiones_mercadeo"]

    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.add(new_role)

    db.commit()


def seed_default_users(db: Session):
    """Crea/actualiza usuarios de prueba para cada rol y programa académico."""
    role_estudiante = db.query(Role).filter(Role.name == "estudiante").first()
    role_secretaria = db.query(Role).filter(Role.name == "secretaria").first()
    role_administrativo = db.query(Role).filter(Role.name == "administrativo").first()
    role_admisiones_mercadeo = db.query(Role).filter(Role.name == "admisiones_mercadeo").first()

    if not role_estudiante or not role_secretaria or not role_administrativo or not role_admisiones_mercadeo:
        return

    def upsert_user(email: str, full_name: str, role_id: int, programa_academico: str | None):
        """Inserta o sincroniza un usuario semilla conservando credenciales de desarrollo."""
        existing_user = db.query(User).filter(User.email == email).first()
        hashed = hashear_contrasena(SEED_PASSWORD)

        if existing_user:
            existing_user.full_name = full_name
            existing_user.role_id = role_id
            existing_user.programa_academico = programa_academico
            existing_user.is_active = True
            existing_user.hashed_password = hashed
            db.commit()
            return

        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed,
            programa_academico=programa_academico,
            is_active=True,
            role_id=role_id,
        )
        db.add(user)
        db.commit()

    upsert_user(
        email="secretaria@uniautonoma.edu.co",
        full_name="Secretaria Ingenierias",
        role_id=role_secretaria.id,
        programa_academico="ingenierias",
    )

    upsert_user(
        email="admisiones.mercadeo@uniautonoma.edu.co",
        full_name="Admisiones y Mercadeo",
        role_id=role_admisiones_mercadeo.id,
        programa_academico=None,
    )

    for programa in PROGRAMAS_ACADEMICOS:
        upsert_user(
            email=f"estudiante.{programa}@uniautonoma.edu.co",
            full_name=f"Estudiante {programa.capitalize()}",
            role_id=role_estudiante.id,
            programa_academico=programa,
        )
        upsert_user(
            email=f"secretaria.{programa}@uniautonoma.edu.co",
            full_name=f"Secretaria {programa.capitalize()}",
            role_id=role_secretaria.id,
            programa_academico=programa,
        )
        upsert_user(
            email=f"administrativo.{programa}@uniautonoma.edu.co",
            full_name=f"Administrativo {programa.capitalize()}",
            role_id=role_administrativo.id,
            programa_academico=programa,
        )