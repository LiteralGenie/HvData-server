from config import paths
from ..errors import NoResultsError
from hvpytils.classes.hv_session import HvSession
from ..models.user import User

from bs4 import BeautifulSoup
from urlpath import URL

import base64, calendar, datetime, re, requests


class UserParser:
    @classmethod
    def from_profile(cls, id: int, session: HvSession) -> User:
        page = cls.fetch_page(id=id, session=session)
        
        user = cls._parse_profile_page(page)
        user.id = id

        return user

    @classmethod
    def from_search(cls, ign: str, session: HvSession) -> User:
        url = str(paths.FORUM_ROOT.add_query(act='members'))

        form_data = dict(name=ign,max_results=50)
        resp = session.post(url, data=form_data)
        page = BeautifulSoup(resp.text, 'html.parser')

        results = page.select('.ipbtable tr:has(> td.row1)')
        if len(results) == 0: raise NoResultsError
        
        for row in results:
            cells = row.select(':scope > td')

            name = cells[0].text
            group = cells[2].text
            joined = cls._parse_joined_date(cells[3].text)

            profile_link = URL(cells[0].select_one('a')['href'])
            id = int(profile_link.form.get_one('showuser'))

            return User(current_name=name, group=group, id=id, joined=joined)

    @classmethod
    def fetch_page(cls, id: int, session: HvSession) -> BeautifulSoup:
        url = str(paths.FORUM_ROOT.add_query(showuser=id))
        page = session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    
    @classmethod
    def _parse_profile_page(cls, page: BeautifulSoup) -> User:
        """Returns partially initialized User"""

        avatar = page.select_one('#profilename ~ div:has(> img)').select_one('img')
        avatar = cls._fetch_image_as_base64(avatar['src'])

        current_name = page.select_one('#profilename').text
        
        postdetails = page.select_one('.postdetails').stripped_strings
        assert len(postdetails) == 2, f'Expected 2 lines but found {len(postdetails)}'
        group, joined = postdetails

        joined = cls._parse_joined_date(joined)

        signature = str(page.select_one('.signature'))

        return User(avatar=avatar, current_name=current_name, group=group, joined=joined, signature=signature)

    @classmethod
    def _fetch_image_as_base64(cls, url: str, session: requests.Session) -> str:
        resp = session.get(url)
        type = resp.headers['Content-Type']
        content = base64.b64encode(resp.content)
        return f'data:{type};base64,{content}'

    @classmethod
    def _parse_joined_date(cls, text: str) -> int:
        # @todo generic date to timestamp
        m = re.search(r'(\d+)-(\w+) (\d+)', text)
        day = int(m.group(1))
        month = cls._month_to_int(m.group(2))
        year = int(m.group(3))

        date = datetime.datetime(year=year, month=month, day=day)
        ts = calendar.timegm(date.timetuple())
        
        return ts

    @classmethod
    def _month_to_int(cls, month: str):
        months = [
            'January', 'February', 'March', 
            'April', 'May', 'June',
            'July', 'August', 'September',
            'October', 'November', 'December'
        ]

        return 1 + months.index(month)