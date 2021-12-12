from hvpytils import HvSession
from ..models.lottery import Lottery, LotteryItem, LotteryType

from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from typing import Tuple
from urlpath import URL

import re

# @todo separate parsing from creation?


class LotteryParser:
    @classmethod
    def fetch(cls, type: LotteryType, id: int, session: HvSession) -> Tuple[Lottery, LotteryItem]:
        page = cls.fetch_page(type=type, id=id, session=session)

        lotto = cls._parse_lotto(page)
        lotto.id = id
        lotto.type = type

        items = cls._parse_lotto_items(page)
        for it in items:
            it.id = id
            it.type = type

            # get / assign user

    @classmethod
    def get_latest(cls, type: LotteryType, session: HvSession) -> Tuple[BeautifulSoup, int]:
        """Get (html,id) for current lottery"""

        page = session.get(type.value)
        soup = BeautifulSoup(page.text, 'html.parser')

        prev_button = soup.select_one('img[src="/y/shops/lottery_prev_a.png"]')
        prev_url = re.search(r"'(http.*)'", prev_button['onclick'])
        prev_url = URL(prev_url.group(1))

        prev_id = prev_url.form.get_one('lottery')
        prev_id = int(prev_id)
        
        return soup, prev_id+1

    @classmethod
    def fetch_page(cls, type: LotteryType, id: int, session: HvSession) -> BeautifulSoup:
        url = type.value + f'&lottery={id}'
        page = session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    @classmethod
    def _parse_lotto(cls, page: BeautifulSoup) -> Lottery:
        """Return partially initialized Lottery"""

        text = page.select_one('#rightpane > div:nth-child(5)').text
        m = re.search(r'You hold \d+ of (\d+) sold tickets.', text)
        tickets = m.group(1)

        if type is LotteryType.WEAPON:
            type_id = 0
        else:
            type_id = 1

        return Lottery(tickets=tickets)

    @classmethod
    def _parse_lotto_items(cls, page: BeautifulSoup) -> Tuple[list[LotteryItem], list[str]]:
        """Return partially intialized list of LotteryItem's"""

        prizes = []
        raw_winners = []

        # parse page
        equip_name = page.select_one('#lottery_eqname').text

        divs = page.select('#leftpane > div:nth-child(4) > div')
        assert len(divs) == 9, f'Expected 9 divs but found {len(divs)}'

        texts = [x.text.split(': ') for x in divs]
        texts = [x[1] for x in texts]

        # grand prize
        equip = LotteryItem(item=equip_name, place=0, quantity=1, winner=texts[0])
        prizes.append(equip)

        # consolation prizes
        items = [texts[2*i + 1] for i in range(4)]
        raw_winners = [texts[2*i + 2] for i in range(4)]

        for i,it in enumerate(items):
            quantity, name = it.split(' ', maxsplit=1)
            conslation_prize = LotteryItem(item=name, place=i+1, quantity=quantity)
            prizes.append(conslation_prize)
        
        # return
        return prizes, raw_winners



from ..models import Base
from sqlalchemy import create_engine

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