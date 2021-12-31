from config import env, secrets
from hvpytils import HvSession, HvCookies

from multiprocessing.connection import Listener
from requests import Request

import logging

# @todo error handling


LOG = logging.getLogger('SessionWorker')
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

with Listener(env.hv_session.address, authkey=secrets.hv_session.authkey) as listener:
    while True:
        with listener.accept() as conn:
            req: Request = conn.recv()
            LOG.info('worker got request', (req.method, req.url), req)
            # @todo log source
            resp = session.send(req)
            conn.send(resp)