from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.basemodel import StartModel


class CharityProject(Base, StartModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
