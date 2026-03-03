from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.revoked_token_repository import RevokedTokenRepository
from app.core.config import ALGORITHM, SECRET_KEY
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.models.role_model import Role

class AuthService:

    ALLOWED_PROGRAMAS = {"ingenierias", "derecho", "finanzas"}

    def __init__(self):
        self.user_repo = UserRepository()
        self.revoked_token_repo = RevokedTokenRepository()

    def _extract_refresh_payload(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as exc:
            raise HTTPException(status_code=401, detail="Refresh token inválido o expirado") from exc

        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=401, detail="Token no válido para renovación")

        sub = payload.get("sub")
        jti = payload.get("jti")
        exp = payload.get("exp")

        if not sub or not jti or exp is None:
            raise HTTPException(status_code=401, detail="Refresh token inválido")

        expires_at = datetime.utcfromtimestamp(exp)

        return {
            "sub": sub,
            "jti": jti,
            "expires_at": expires_at,
        }

    def _build_token_pair(self, email: str, role: str) -> dict:
        token_payload = {"sub": email, "role": role}
        return {
            "access_token": create_access_token(token_payload),
            "refresh_token": create_refresh_token(token_payload),
            "token_type": "bearer",
        }

    def register(
        self,
        db: Session,
        full_name: str,
        email: str,
        password: str,
        programa_academico: str | None = None,
    ):
        if self.user_repo.get_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email ya registrado")

        hashed_password = hash_password(password)

        default_role = db.query(Role).filter(Role.id == 2).first()
        if not default_role:
            raise HTTPException(status_code=500, detail="Rol por defecto no configurado")

        if default_role.name == "estudiante":
            if programa_academico is None:
                raise HTTPException(status_code=400, detail="programa_academico es obligatorio para estudiantes")
            if programa_academico not in self.ALLOWED_PROGRAMAS:
                raise HTTPException(status_code=400, detail="programa_academico inválido")
        else:
            programa_academico = None

        user = self.user_repo.create(
            db=db,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role_id=default_role.id,
            programa_academico=programa_academico,
        )

        tokens = self._build_token_pair(email=user.email, role=user.role.name)

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "programa_academico": user.programa_academico,
                "is_active": user.is_active,
                "created_at": user.created_at,
            },
            **tokens,
        }

    def login(self, db: Session, email: str, password: str):
        user = self.user_repo.get_by_email(db, email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        tokens = self._build_token_pair(email=user.email, role=user.role.name)

        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "programa_academico": user.programa_academico,
                "is_active": user.is_active,
                "created_at": user.created_at,
            },
            **tokens,
        }

    def refresh(self, db: Session, refresh_token: str) -> dict:
        refresh_payload = self._extract_refresh_payload(refresh_token)

        if self.revoked_token_repo.is_revoked(db, refresh_payload["jti"]):
            raise HTTPException(status_code=401, detail="Refresh token revocado")

        user = self.user_repo.get_by_email(db, refresh_payload["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        self.revoked_token_repo.revoke(
            db=db,
            jti=refresh_payload["jti"],
            expires_at=refresh_payload["expires_at"],
        )

        return self._build_token_pair(email=user.email, role=user.role.name)

    def logout(self, db: Session, refresh_token: str) -> dict:
        refresh_payload = self._extract_refresh_payload(refresh_token)

        self.revoked_token_repo.revoke(
            db=db,
            jti=refresh_payload["jti"],
            expires_at=refresh_payload["expires_at"],
        )

        return {"detail": "Sesión cerrada correctamente"}