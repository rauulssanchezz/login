from sqlalchemy import select
from app.database import DB_DEPENDENCY
from app.models.app_user_model import AppUserModel, pwd_context
from app.schemas.app_user_schema import AppUserSchema
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

secret_key = str(os.getenv('SECRET_KEY'))
algorithm = str(os.getenv('ALGORITHM'))
access_token_expire_minutes = int(str(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))

class AuthService:

    @staticmethod
    async def signup_user(user: AppUserModel, db: DB_DEPENDENCY):
        new_user = AppUserSchema(
            name = user.name,
            email = user.email,
            password = user.password
        )

        db.add(new_user)
        await db.commit()

    @staticmethod
    async def login(user: AppUserModel, db: DB_DEPENDENCY):
        result = await db.execute(
            select(AppUserSchema).where(AppUserSchema.email == user.email)
        )

        user_log = result.scalars().first()

        if not pwd_context.verify(user.password, user_log.password): # type: ignore
            raise ValueError('Las contraseñas no coinciden.')
        
        expire = datetime.now() + timedelta(minutes=access_token_expire_minutes)
        payload = {
            "sub": user_log.id, # type: ignore
            "exp": expire
        }
        token = jwt.encode(payload, secret_key, algorithm=algorithm)

        return {'access_token': token, 'token_type': 'bearer', 'user_data': user_log}
        