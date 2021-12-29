from fastapi import Depends, FastAPI
from .dependencies import session


app = FastAPI(
    dependencies=[Depends(lambda: session)]
)