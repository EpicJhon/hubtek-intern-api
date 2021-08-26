import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Dog(Base):
    __tablename__ = 'dogs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    picture = Column(String, index=True, default=None)
    create_date = Column(DateTime, default=datetime.datetime.now)
    is_adopted = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='dogs')
