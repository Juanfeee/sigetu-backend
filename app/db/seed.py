from sqlalchemy.orm import Session
from app.models.role_model import Role

def seed_roles(db: Session):
    roles = ["admin", "estudiante", "secretaria"]

    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.add(new_role)

    db.commit()