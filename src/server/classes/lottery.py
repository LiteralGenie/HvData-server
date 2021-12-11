from sqlalchemy.sql.schema import ForeignKeyConstraint
from config import paths
from hvpytils import HvSession

from bs4 import BeautifulSoup
from enum import Enum
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.types import Integer, String
from typing import Tuple
from urlpath import URL

import re


Base = declarative_base()

class Lottery(Base):
    __tablename__ = 'lottery'

    id: int = Column(Integer, primary_key=True)
    tickets: int = Column(Integer)
    type: int = Column(Integer, primary_key=True)

class LotteryItem(Base):
    __tablename__ = 'lottery_item'
    __table_args__ = (
        ForeignKeyConstraint(['id', 'type'], [Lottery.id, Lottery.type]),
    )

    id: int = Column(Integer, primary_key=True)
    item: str = Column(String)
    place: int = Column(Integer, primary_key=True)
    quantity: int = Column(Integer)
    type: int = Column(Integer, primary_key=True)
    winner: str = Column(String)

class LotteryType(Enum):
    WEAPON = str(paths.HV_LOTTO_WEAPON)
    ARMOR = str(paths.HV_LOTTO_ARMOR)

def get_latest_lotto(type: LotteryType, session: HvSession) -> Tuple[BeautifulSoup, int]:
    page = session.get(type.value)
    soup = BeautifulSoup(page.text, 'html.parser')

    prev_button = soup.select_one('img[src="/y/shops/lottery_prev_a.png"]')
    prev_url = re.search(r"'(http.*)'", prev_button['onclick'])
    prev_url = URL(prev_url.group(1))

    prev_id = prev_url.form.get_one('lottery')
    prev_id = int(prev_id)
    
    return soup, prev_id+1

def parse_lotto(id: int, type: LotteryType, page: BeautifulSoup) -> Lottery:
    text = page.select_one('#rightpane > div:nth-child(5)').text
    m = re.search(r'You hold \d+ of (\d+) sold tickets.', text)
    tickets = m.group(1)

    if type is LotteryType.WEAPON:
        type_id = 0
    else:
        type_id = 1

    return Lottery(id=id, type=type_id, tickets=tickets)

def parse_lotto_items(id: int, type: LotteryType, page: BeautifulSoup) -> list[LotteryItem]:
    prizes = []

    # parse page
    equip_name = page.select_one('#lottery_eqname').text

    divs = page.select('#leftpane > div:nth-child(4) > div')
    assert len(divs) == 9, f'Expected 9 divs but found {len(divs)}'

    texts = [x.text.split(': ') for x in divs]
    texts = [x[1] for x in texts]

    # generate items
    if type is LotteryType.WEAPON:
        type_id = 0
    else:
        type_id = 1

    equip = LotteryItem(id=id, type=type_id, item=equip_name, place=0, quantity=1, winner=texts[0])
    prizes.append(equip)

    for i in range(0,4):
        item = texts[2*i + 1]
        winner = texts[2*i + 2]

        name,quantity = item.split(' ', maxsplit=1)
        conslation_prize = LotteryItem(id=id, type=type_id, item=name, place=i+1, quantity=quantity, winner=winner)
        prizes.append(conslation_prize)
    
    # return
    return prizes

def fetch_lotto_page(type: LotteryType, id: int, session: HvSession) -> BeautifulSoup:
    url = type.value + f'&lottery={id}'
    page = session.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

hv_session = HvSession(user='frotag', pw='A1S2d3f4')
hv_session.login()

db = create_engine("sqlite:///sanity.sqlite", echo=True)
Base.metadata.create_all(db)

with Session(db) as db_session:
    with db_session.begin():
        _, newest_id = get_latest_lotto(LotteryType.WEAPON, hv_session)
        
        soup = fetch_lotto_page(LotteryType.WEAPON, newest_id-1, hv_session)
        lotto = parse_lotto(newest_id-1, LotteryType.WEAPON, soup)
        items = parse_lotto_items(newest_id-1, LotteryType.WEAPON, soup)

        db_session.add(lotto)
        [db_session.add(x) for x in items]

resp,id = get_latest_lotto(LotteryType.WEAPON, hv_session)
pass
