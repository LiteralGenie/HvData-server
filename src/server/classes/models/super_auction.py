from . import Base
from .user import User
from .uuid_mixin import UuidMixin

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class SuperAuction(Base, UuidMixin):
    __tablename__ = 'super_auction'
    
    id: int = Column(Integer, primary_key=True)

    end_date: Float = Column(Float, nullable=False)
    number: str = Column(String, nullable=False)

class SuperAuctionItem(Base, UuidMixin):
    __tablename__ = 'super_auction_item'

    auction_id: int = Column(Integer, ForeignKey('super_auction.id'), primary_key=True)
    auction = relationship('SuperAuction', backref='items')

    category: str = Column(String, primary_key=True)
    number: int = Column(Integer, primary_key=True)

    description: str = Column(String)
    name: str = Column(String, nullable=False)
    price: int = Column(Integer, nullable=False)

    equip_id: int = Column(Integer, ForeignKey('equip.id'))
    equip_key: int = Column(Integer, ForeignKey('equip.id'))
    item_name: str = Column(String)
    item_quantity: int = Column(Integer)

    buyer_raw: str = Column(String)
    buyer_id: int = Column(Integer, ForeignKey('user.id'))
    buyer: User = relationship('User', backref='super_auction_buys', foreign_keys=[buyer_id])

    seller_raw: str = Column(String, nullable=False)
    seller_id: int = Column(Integer, ForeignKey('user.id'))
    seller: User = relationship('User', backref='super_auction_sells', foreign_keys=[seller_id])
