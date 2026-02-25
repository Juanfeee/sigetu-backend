from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Annotated[str, constr(min_length=3, max_length=50)]
    password: Annotated[str, constr(min_length=8, max_length=128)]

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True