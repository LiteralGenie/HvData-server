from fastapi import APIRouter, Request


router = APIRouter()

@router.get('/lottery/{id}')
def get_lottery(id: int, request: Request):
    hv_session = request.app.state.hv_session
    