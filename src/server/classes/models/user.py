from . import Base

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'user'

    avatar: str = Column(String)
    current_name: str = Column(String, nullable=False)
    group: str = Column(String)
    id: int = Column(Integer, primary_key=True)
    joined: int = Column(Integer)
    signature: str = Column(String)