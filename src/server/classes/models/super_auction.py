from . import Base
from .equip import Equip
from .user import User

from sqlalchemy import Column, Float, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship


class SuperAuction(Base):
    __tablename__ = 'super_auction'
    
    id: int = Column(Integer, primary_key=True)

    end_date: Float = Column(Float, nullable=False)
    number: str = Column(String, nullable=False)

class SuperAuctionItem(Base):
    __tablename__ = 'super_auction_item'
    __table_args__ = (
        # composite foreign keys need to be at least this ugly
        ForeignKeyConstraint(['id', 'type'], [Equip.id, Equip.key]),
    )

    auction: SuperAuction = Column(SuperAuction, ForeignKey('super_auction.id'), primary_key=True)
    cat: str = Column(String, primary_key=True)
    number: int = Column(Integer, primary_key=True)
    
    description: str = Column(String)
    name: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)

    item_name: str = Column(String)
    item_quantity: int = Column(Integer)
    
    equip_id: int = Column(Integer, ForeignKey('equip.id'))

    buyer_raw: str = Column(String, nullable=False)
    buyer_id: int = Column(Integer, ForeignKey('user.id'))
    buyer: User = relationship('User', backref='super_auction_buys')

    seller_raw: str = Column(String, nullable=False)
    seller_id: int = Column(Integer, ForeignKey('user.id'))
    seller: User = relationship('User', backref='super_auction_sells')
