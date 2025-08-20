import uuid
from sqlalchemy import Column, String, Uuid
from app.database import Base

class AppUserSchema(Base):
    __tablename__ = 'app_user'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
