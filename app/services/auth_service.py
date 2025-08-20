from sqlalchemy import select
from app.database import DB_DEPENDENCY
from app.models.app_user_model import AppUserModel, pwd_context
from app.schemas.app_user_schema import AppUserSchema


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
        
        return user_log