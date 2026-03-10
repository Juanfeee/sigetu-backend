"""Repositorio para control de refresh tokens revocados."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.modelo_token_revocado import RevokedToken


class RepositorioTokensRevocados:
    """Gestiona la lista de revocación usada en logout y refresh seguro."""

    def esta_revocado(self, db: Session, jti: str) -> bool:
        """Indica si un token refresh ya fue revocado previamente."""
        return db.query(RevokedToken).filter(RevokedToken.jti == jti).first() is not None

    def revocar(self, db: Session, jti: str, expires_at: datetime) -> RevokedToken:
        """Registra un token como revocado para bloquear reutilización."""
        existente = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
        if existente:
            return existente

        token = RevokedToken(jti=jti, expires_at=expires_at)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token
