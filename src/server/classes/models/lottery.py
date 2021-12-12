from . import Base
from config import paths
from .user import User

from enum import Enum
from sqlalchemy import Column, Enum, ForeignKey, ForeignKeyConstraint, Integer, String

# @todo check logging
# @todo users
# @todo type to int

class LotteryType(Enum):
    WEAPON = str(paths.HV_LOTTO_WEAPON)
    ARMOR = str(paths.HV_LOTTO_ARMOR)

class Lottery(Base):
    __tablename__ = 'lottery'

    id: int = Column(Integer, primary_key=True)
    tickets: int = Column(Integer, nullable=False)
    type: LotteryType = Column(Enum(LotteryType), primary_key=True)

class LotteryItem(Base):
    __tablename__ = 'lottery_item'
    __table_args__ = (
        # composite foreign keys need to be at least this ugly
        ForeignKeyConstraint(['id', 'type'], [Lottery.id, Lottery.type]),
    )

    id: int = Column(Integer, primary_key=True)
    item: str = Column(String, nullable=False)
    place: int = Column(Integer, primary_key=True)
    quantity: int = Column(Integer, nullable=False)
    type: LotteryType = Column(Enum(LotteryType), primary_key=True) 
    user_id: User = Column(Integer, ForeignKey('user.id'), nullable=False)