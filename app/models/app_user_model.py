from typing import Optional
from pydantic import BaseModel, EmailStr

class AppUserModel(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str