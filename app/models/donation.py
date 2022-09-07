from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.basemodel import StartModel


class Donation(Base, StartModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
