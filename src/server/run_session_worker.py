from config import env, paths, secrets
from hvpytils import HvSession, HvCookies

from multiprocessing.connection import Listener
from requests import Request

import logging

# @todo error handling


LOG = logging.getLogger('HvSession')
LOG.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
LOG.addHandler(handler)


login_info = HvCookies(
    ipb_member_id=secrets.hv_session.ipb_member_id, 
    ipb_pass_hash=secrets.hv_session.ipb_pass_hash
)
session = HvSession(cookies=login_info)
session.login()
resp = session.get(session.HV_LINK)

with Listener(env.session_address, authkey=secrets.hv_session.authkey) as listener:
    with listener.accept() as conn:
        while True:
            req: Request = conn.recv()
            # @todo log source
            
            resp = session.send(req)

            conn.send(resp)