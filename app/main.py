from app.db.seed import seed_roles
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.api.routes import auth_routes


app = FastAPI()

app.include_router(auth_routes.router)
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_roles(db)
    db.close()