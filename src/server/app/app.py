from fastapi import Depends, FastAPI
from sqlalchemy.engine import create_engine

from classes.client_session import ClientSession
from .fetcher import Fetcher


app = FastAPI(debug=True, )

@app.on_event('startup')
async def on_startup():
    hv_session = ClientSession()
    db = create_engine('sqlite:///hvdata.sqlite', echo=True)
    
    app.state.hv_session = hv_session
    app.state.db = db
