from config import paths
from ..models.super_auction import SuperAuction, SuperAuctionItem
from utils.date_utils import utc_date_to_timestamp

from bs4 import BeautifulSoup
from hvpytils import EquipParser
from urlpath import URL

import re, requests


class SuperParser:
    session: requests.Session

    def __init__(self, session: requests.Session):
        self.session = session

    def fetch_list(self) -> list[SuperAuction]:
        page = self._get(paths.SUPER_ROOT)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, 'html.parser')

        rows = soup.select('tbody > tr')
        rows = [r.select('td') for r in rows]
        assert all(len(r) == 6 for r in rows)

        aucs = []
        for r in rows:
            number = r[0].text
            
            tmp = r[1].text.split('-') # MM-DD-YYYY
            end_date = utc_date_to_timestamp(tmp[2], tmp[0], tmp[1])

            id = r[2].replace('itemlist', '') # itemlist######
            id = int(id)

            aucs.append(SuperAuction(id=id, end_date=end_date, number=number))

        return aucs

    def parse_page(self, auction_id: int, soup: BeautifulSoup) -> list[SuperAuctionItem]:
        """
        Extract items from https://reasoningtheory.net/itemlist######
        """

        items = self._parse_page(soup=soup)
        for it in items: it.auction = auction_id
        
        return items

    def _parse_page(self, soup: BeautifulSoup) -> list[SuperAuctionItem]:
        tables = soup.select('table.itemSection')
        
        rows = []
        for tbl in tables:
            # split item table into cells
            rows = tbl.select('tbody > tr')
            rows = [r.select('td') for r in rows]
            assert all(len(r) == 6 for r in rows)

            # determine item category
            cat = [x[0].text for x in rows]
            cat = [self._parse_code(x)[0] for x in cat]
            assert(c == cat[0] for c in cat)
            cat = cat[0]

            # isolate the ugly parsing logic
            item_lst = [self._parse_row(r) for r in rows]
            rows.extend(item_lst)
        
        return rows

    def fetch_auction(self, id: id):
        url = str(paths.SUPER_LIST) + str(id)
        page = self._get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return self.parse_page(soup)

    def _get(self, url: str|URL):
        resp = self.session.get(str(url))
        resp.encoding = 'utf-8'
        return resp
    
    def _parse_row(self, tds: list[BeautifulSoup]):
        item = SuperAuctionItem()
        
        # parse category-specific attrs
        if item.category == 'mat':
            m = re.match(r'(\d+) (.+)', tds[1].text)
            item.quantity = int(m.group(1))
            item.name = m.group(2)
        else:
            link = tds[1].select_one('a')['href']
            parsed_link = EquipParser.parse_equip_url(link)
            
            item.name = tds[1].text
            item.equip_id = parsed_link[0]
            item.equip_key = parsed_link[1]
        
        # parse winning bid info
        current_bid = tds[3].text
        if current_bid == '0':
            item.price = 0
        else:
            patt = r'(\d+)k \((.*) #[\d.]+\)'
            m = re.match(patt, tds[3].text)
            price, buyer = m.groups()

            item.price = 1000 * int(price)
            item.buyer_raw = buyer
        
        parsed_code = self._parse_code(tds[0].text)
        
        item.category = parsed_code[0]
        item.descripton = tds[2].text
        item.number = parsed_code[1]
        item.seller = tds[5].text

        return item


    def _parse_code(self, text) -> tuple[str, int]:
        """
        Extract 
          - item category (lowercase + trimmed)
          - item code
        """
        
        m = re.match(r'(\w+)(\d+)', text)
        cat = m.group(1).lower().trim()
        number = int(m.group(2))

        return cat, number