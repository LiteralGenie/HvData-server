from classes import errors
from classes.models import SuperAuction, SuperAuctionItem
from ..fetcher import Fetcher
from .super_dto import SuperAuctionDto

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/super',
    tags=["Auctions (superlatanium)"]
)

@router.get('/latest', response_model=SuperAuctionDto, response_model_exclude={'items'})
def _(request: Request):
    fetcher: Fetcher = request.app.state.db_fetcher
    with fetcher.super_list() as aucs:
        resp = [
            SuperAuctionDto.serialize(x, wrap_response=False, include_items=False)
            for x in aucs
        ]
        return JSONResponse(content=resp)

@router.get('/{id}', response_model=SuperAuctionDto)
def _(id: int, request: Request):
    fetcher: Fetcher = request.app.state.db_fetcher
    auc = fetcher.super_auction(id=id)
    return SuperAuctionDto.serialize(auc)