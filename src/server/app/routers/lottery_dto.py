from classes.models import Lottery, LotteryItem, LotteryType, User
from . import _roll

from enum import Enum
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import random


class LotteryTypeDto(str, Enum):
    WEAPON = 'weapon'
    ARMOR = 'armor'

class LotteryUserDto(BaseModel):
    name: str
    id: Optional[int]

    @classmethod
    def serialize(cls, user: User):
        if user is None: 
            return None
        else:
            return dict(
                name = user.current_name,
                id = user.id
            )

class LotteryItemDto(BaseModel):
    name: str
    place: int
    quantity: int
    winner: LotteryUserDto
        
    @classmethod
    def serialize(cls, it: LotteryItem):
        if it.winner:
            winner = LotteryUserDto.serialize(it.winner)
        else:
            winner = dict(name=it.raw_winner, id=None)

        return dict(
            name = it.name,
            place = it.place,
            quantity = it.quantity,
            winner = winner
        )

class LotteryDto(BaseModel):
    id: int
    type: LotteryTypeDto
    tickets: int
    items: list[LotteryItemDto]

    @classmethod
    def serialize(cls, l: Lottery):
        return JSONResponse(content=dict(
            id = l.id,
            type = getattr(LotteryTypeDto, l.type.name).value,
            tickets = l.tickets,
            items = [LotteryItemDto.serialize(x) for x in l.items]
        ))


def _get_sample(grand_prize='grand prize'):
    users = _roll.users()
    ids = random.choices(list(range(1, 10**7)), k=5)

    return dict(
        id=random.randint(1,10000),
        type=LotteryTypeDto.WEAPON,
        tickets=random.randint(10**4, 10**8),
        items=[
            dict(
                name=grand_prize,
                place=0,
                quantity=1,
                winner=dict(name='프레이', id=ids.pop())
            ),
            dict(
                name='Golden Lottery Tickets',
                place=1,
                quantity=4,
                winner=dict(name=users.pop(), id=None)
            ),
            dict(
                name='Caffeinated Candies',
                place=2,
                quantity=16,
                winner=dict(name=users.pop(), id=ids.pop())
            ),
            dict(
                name='Chaos Tokens',
                place=3,
                quantity=160,
                winner=dict(name=users.pop(), id=ids.pop())
            ),
            dict(
                name='Chaos Tokens',
                place=4,
                quantity=160,
                winner=dict(name=users.pop(), id=ids.pop())
            )
        ]
    )

class examples:
    get_weapon = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'value':{
                                **_get_sample(grand_prize='Peerless Hallowed Oak Staff of Heimdall'),
                                'type': LotteryTypeDto.WEAPON
                            }
                        }
                    }
                }
            }
        },

        422: {
            'description': 'Invalid Lottery Id'
        }
    }

    get_armor = {
        200: {
            'description': 'Success',
            'content': {
                'application/json': {
                    'examples': {
                        '1': {
                            'value':{
                                **_get_sample(grand_prize='Peerless Mystic Phase Robe of Fenrir'),
                                'type': LotteryTypeDto.ARMOR
                            }
                        }
                    }
                }
            }
        },

        422: {
            'description': 'Invalid Lottery Id'
        }
    }