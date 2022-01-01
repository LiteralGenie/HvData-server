from classes import errors
from classes.models import Lottery, LotteryItem, LotteryType
from ..fetcher import Fetcher
from .lottery_dto import LotteryDto, examples

from fastapi import APIRouter, HTTPException, Request


router = APIRouter(
    prefix='/lottery'
)

@router.get('/armor/{id}', response_model=LotteryDto, responses=examples.get_armor)
def armor_lottery(id: int, request: Request):
    try:
        fetcher: Fetcher = request.app.state.db_fetcher
        lotto = fetcher.lottery(id=id, type=LotteryType.ARMOR)
        return LotteryDto.serialize(lotto)
    except errors.UnparsablePageError:
        return HTTPException(status_code=422, detail='Out of range')

@router.get('/weapon/{id}', response_model=LotteryDto, responses=examples.get_weapon)
def weapon_lottery(id: int, request: Request):
    try:
        fetcher: Fetcher = request.app.state.db_fetcher
        lotto = fetcher.lottery(id=id, type=LotteryType.WEAPON)
        return LotteryDto.serialize(lotto)
    except errors.UnparsablePageError:
        return HTTPException(status_code=422, detail='Out of range')