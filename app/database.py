from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from fastapi import Depends
from dotenv import load_dotenv
from typing import Annotated
import os

load_dotenv()

db_type: str = str(os.getenv("DATABASE_TYPE"))
db_user: str = str(os.getenv("DATABASE_USER"))
db_password: str = str(os.getenv("DATABASE_PASSWORD"))
db_host: str = str(os.getenv("DATABASE_HOST"))
db_port: str = str(os.getenv("DATABASE_PORT"))
db_name: str = str(os.getenv("DATABASE_NAME"))

SQLALCHEMY_DATABASE_URL = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with async_session() as db:
        yield db

DB_DEPENDENCY = Annotated[AsyncSession, Depends(get_db)]