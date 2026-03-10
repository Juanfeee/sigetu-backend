"""Modelo ORM para registrar refresh tokens revocados."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class RevokedToken(Base):
    """Token revocado identificado por `jti` para bloquear reutilización."""
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(64), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    revoked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
