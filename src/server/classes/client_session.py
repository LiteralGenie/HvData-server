from hvpytils import HvSession

from multiprocessing.connection import Client


class ClientSession(HvSession):
    """
    The login process and all other requests are performed remotely. 
    You do not need to supply HV cookies / credentials to this class. Instead, supply the remote server address and authkey.
    """

    RATE_LIMIT = 0

    authkey: str
    server_address: tuple[str, int]

    def __init__(self, server_address: tuple[str, int], authkey: str, **kwargs):
        super().__init__(**kwargs)
        self.server_address = server_address
        self.authkey = authkey

    def send(self, req):
        with Client(self.server_address, authkey=self.authkey) as conn:
            conn.send(req)
            resp = conn.recv()
            return resp