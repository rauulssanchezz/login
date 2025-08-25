from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.database import DB_DEPENDENCY
from app.models.app_user_model import AppUserModel
from app.schemas.app_user_schema import AppUserSchema
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

load_dotenv()

secret_key = str(os.getenv('SECRET_KEY'))
algorithm = str(os.getenv('ALGORITHM'))
access_token_expire_minutes = int(str(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))

class AuthService:
    @staticmethod
    async def verify_token(token: str):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            user_id = payload.get("sub")

            if user_id is None:
                raise ValueError("Token inválido: no contiene sub.")
            
            return {"valid": True, "user_id": user_id}
        
        except Exception as e:
            return {"valid": False, "error": str(e)}

    @staticmethod
    async def signup_user(user: AppUserModel, db: DB_DEPENDENCY):
        try:
            new_user = AppUserSchema(
                name = user.name,
                email = user.email,
                password = pwd_context.hash(user.password)
            )

            db.add(new_user)
            await db.commit()

            return {'success': 'Usuario creado con exito.'}
        except IntegrityError:
            raise ValueError('Ya existe un usuario con ese email.')
        except Exception as e:
            raise ValueError(str(e))

    @staticmethod
    async def login(user: AppUserModel, db: DB_DEPENDENCY):
        try:
            result = await db.execute(
            select(AppUserSchema).where(AppUserSchema.email == user.email)
            )

            user_log = result.scalars().first()

            if not pwd_context.verify(user.password, user_log.password): # type: ignore
                raise ValueError('Las contraseñas no coinciden.')
            
            expire = datetime.now() + timedelta(minutes=access_token_expire_minutes)
            payload = {
                "sub": str(user_log.id), # type: ignore
                "exp": expire
            }
            token = jwt.encode(payload, secret_key, algorithm=algorithm)

            return {'access_token': token, 'token_type': 'bearer', 'user_data': user_log}
        except Exception as e:
            raise ValueError(str(e))    