from classes.models import SuperAuction, SuperAuctionItem, User
from classes.parsers import SuperParser
from . import _roll

from enum import Enum
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import random


class SuperAuctionUserDto(BaseModel):
    name: str
    uuid: str

    @classmethod
    def serialize(cls, user: User):
        if user is None: 
            return None
        else:
            return dict(
                name = user.current_name,
                uuid = user.uuid
            )

class SuperAuctionItemDto(BaseModel):
    category: str
    number: int

    name: str
    description: str
    price: int
    quantity: int

    equip_id: Optional[int]
    equip_key: Optional[str]

    buyer: Optional[SuperAuctionUserDto]
    seller: SuperAuctionUserDto

    @classmethod
    def serialize(cls, it: SuperAuctionItem):
        if it.buyer:
            buyer = SuperAuctionUserDto.serialize(it.buyer)
        else:
            if it.buyer_raw:
                buyer = dict(name=it.buyer_raw, uuid=it.uuid + '_b')
            else:
                buyer = None

        if it.seller:
            seller = SuperAuctionUserDto.serialize(it.seller)
        else:
            seller = dict(name=it.seller_raw, uuid=it.uuid + '_s')
        
        return dict(
            category = it.category,
            number = it.number,

            description = it.description,
            name = it.name,
            price = it.price,
            quantity = it.quantity,

            equip_id = it.equip_id,
            equip_key = it.equip_key,

            buyer = buyer,
            seller = seller
        )

class SuperAuctionDto(BaseModel):
    id: int
    end_date: float
    number: str
    items: Optional[list[SuperAuctionItemDto]]

    @classmethod
    def serialize(cls, auc: SuperAuction, wrap_response=True, include_items=True):
        result = dict(
            id = auc.id,
            end_date = auc.end_date,
            number = auc.number
        )

        if include_items:
            result['items'] = [SuperAuctionItemDto.serialize(x) for x in auc.items]

        if wrap_response:
            result = JSONResponse(content=result)

        return result

# def _sample_lotto(grand_prize='grand prize'):
#     users = _roll.users()
#     uuids = random.choices(list(range(1, 10**7)), k=5)

#     return dict(
#         id=random.randint(1,10000),
#         type=LotteryTypeDto.WEAPON,
#         tickets=random.randint(10**4, 10**8),
#         items=[
#             dict(
#                 name=grand_prize,
#                 place=0,
#                 quantity=1,
#                 winner=dict(name='프레이', uuid=uuids.pop())
#             ),
#             dict(
#                 name='Golden Lottery Tickets',
#                 place=1,
#                 quantity=4,
#                 winner=dict(name=users.pop(), uuid=uuids.pop())
#             ),
#             dict(
#                 name='Caffeinated Candies',
#                 place=2,
#                 quantity=16,
#                 winner=dict(name=users.pop(), uuid=uuids.pop())
#             ),
#             dict(
#                 name='Chaos Tokens',
#                 place=3,
#                 quantity=160,
#                 winner=dict(name=users.pop(), uuid=uuids.pop())
#             ),
#             dict(
#                 name='Chaos Tokens',
#                 place=4,
#                 quantity=160,
#                 winner=dict(name=users.pop(), uuid=uuids.pop())
#             )
#         ]
#     )

# class examples:
#     get_weapon = {
#         200: {
#             'description': 'Success',
#             'content': {
#                 'application/json': {
#                     'examples': {
#                         '1': {
#                             'value': {
#                                 **_sample_lotto(grand_prize='Peerless Hallowed Oak Staff of Heimdall'),
#                                 'type': LotteryTypeDto.WEAPON
#                             }
#                         }
#                     }
#                 }
#             }
#         },

#         422: {
#             'description': 'Invalid Lottery Id'
#         }
#     }

#     get_armor = {
#         200: {
#             'description': 'Success',
#             'content': {
#                 'application/json': {
#                     'examples': {
#                         '1': {
#                             'value': {
#                                 **_sample_lotto(grand_prize='Peerless Mystic Phase Robe of Fenrir'),
#                                 'type': LotteryTypeDto.ARMOR
#                             }
#                         }
#                     }
#                 }
#             }
#         },

#         422: {
#             'description': 'Invalid Lottery Id'
#         }
#     }

#     get_latest_armor = {
#         200: {
#             'description': 'Success',
#             'content': {
#                 'application/json': {
#                     'examples': {
#                         '1': {
#                             'description': 'The first armor lottery started at 1396094400s epoch time.',
#                             'value': dict(
#                                 id = 101,
#                                 start = LotteryParser.START_DATES[LotteryType.ARMOR] + 100*86400
#                             )
#                         }
#                     }
#                 }
#             }
#         }
#     }

#     get_latest_weapon = {
#         200: {
#             'description': 'Success',
#             'content': {
#                 'application/json': {
#                     'examples': {
#                         '1': {
#                             'description': 'The first weapon lottery started at 1379116800s epoch time.',
#                             'value': dict(
#                                 id = 101,
#                                 start = LotteryParser.START_DATES[LotteryType.WEAPON] + 100*86400
#                             )
#                         }
#                     }
#                 }
#             }
#         }
#     }