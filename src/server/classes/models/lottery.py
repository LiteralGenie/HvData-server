from . import Base
from config import paths
from .user import User

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

import enum, sqlalchemy

# @todo check logging
# @todo users
# @todo type to int

class LotteryType(enum.Enum):
    WEAPON = str(paths.HV_LOTTO_WEAPON)
    ARMOR = str(paths.HV_LOTTO_ARMOR)

class Lottery(Base):
    __tablename__ = 'lottery'

    id: int = Column(Integer, primary_key=True)
    type: LotteryType = Column(sqlalchemy.Enum(LotteryType), primary_key=True)

    tickets: int = Column(Integer, nullable=False)

    items = relationship('LotteryItem', back_populates='lottery')
    
class LotteryItem(Base):
    __tablename__ = 'lottery_item'
    __table_args__ = (
        # composite foreign keys need to be at least this ugly
        ForeignKeyConstraint(['id', 'type'], [Lottery.id, Lottery.type]),
    )

    id: int = Column(Integer, primary_key=True)
    type: LotteryType = Column(sqlalchemy.Enum(LotteryType), primary_key=True) 

    item: str = Column(String, nullable=False)
    place: int = Column(Integer, primary_key=True)
    quantity: int = Column(Integer, nullable=False)

    winner_id: User = Column(Integer, ForeignKey('user.id'), nullable=False)
    winner = relationship('User', backref='lottery_items')

    lottery = relationship('Lottery', back_populates='items')
