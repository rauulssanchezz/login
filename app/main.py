from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.schemas.app_user_schema import AppUserSchema
from app.routers.auth_router import router as auth_router

@asynccontextmanager
async def create_tables(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title='Login',
    lifespan = create_tables
)

app.include_router(auth_router)
