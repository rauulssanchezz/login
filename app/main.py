from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.schemas.app_user_schema import AppUserSchema

@asynccontextmanager
async def create_tables(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title='Login',
    lifespan = create_tables
)
