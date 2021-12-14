from . import Base

from sqlalchemy import Column, Float, Integer, String


class User(Base):
    __tablename__ = 'user'

    avatar: str = Column(String)
    current_name: str = Column(String, nullable=False)
    group: str = Column(String)
    id: int = Column(Integer, primary_key=True)
    joined: float = Column(Float)
    signature: str = Column(String)

# class NameChange(Base):
#     pass