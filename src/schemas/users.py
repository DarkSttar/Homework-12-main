from typing import Optional

from datetime import datetime
from typing import List,Optional
from pydantic import BaseModel,Field,EmailStr


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=8)
    email: EmailStr

class UserResponse(BaseModel):
    pass
    id: int = 1
    username:str
    email:EmailStr
    class Config:
        from_atributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
