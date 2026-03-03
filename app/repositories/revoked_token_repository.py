from datetime import datetime

from sqlalchemy.orm import Session

from app.models.revoked_token_model import RevokedToken


class RevokedTokenRepository:
    def is_revoked(self, db: Session, jti: str) -> bool:
        return db.query(RevokedToken).filter(RevokedToken.jti == jti).first() is not None

    def revoke(self, db: Session, jti: str, expires_at: datetime) -> RevokedToken:
        existing = db.query(RevokedToken).filter(RevokedToken.jti == jti).first()
        if existing:
            return existing

        token = RevokedToken(jti=jti, expires_at=expires_at)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token
