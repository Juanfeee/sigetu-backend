from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, db: Session, name: str, email: str, password: str):

        if self.user_repo.get_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email ya registrado")

        hashed_password = hash_password(password)

        user = self.user_repo.create(
            db=db,
            name=name,
            email=email,
            password=hashed_password
        )

        token = create_access_token({"sub": user.email})

        return token

    def login(self, db: Session, email: str, password: str):

        user = self.user_repo.get_by_email(db, email)

        if not user:
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        token = create_access_token({"sub": user.email})

        return token