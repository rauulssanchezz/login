from pydantic import BaseModel, EmailStr, field_validator
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AppUserModel(BaseModel):
    name: str
    email: EmailStr
    password: str

@field_validator('password')
@classmethod
def hash_password(cls, v):
    return pwd_context.hash(v)