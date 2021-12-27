from classes.parsers.lottery_parser import LotteryParser, LotteryType
from classes.client_session import ClientSession

from config import env, secrets


session = ClientSession(server_address=env.hv_session.address, authkey=secrets.hv_session.authkey)
parser = LotteryParser(session)

result = parser.fetch_partial(LotteryType.WEAPON, 1234)
pass