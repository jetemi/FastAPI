from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    name: str
    price: int
    it_sale: bool
    inventory: int
    created_at: Optional[datetime]

class UpdateBase(BaseModel):
    name: Optional[str]
    price: Optional[int]
    it_sale: Optional[bool]
    inventory: Optional[int] = 0


class Userout(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserLogin(CreateUser):
    pass

class ResponseBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[int]
    owner: Userout

    class Config:
        orm_mode = True

# to confirm that a token is still valid
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None