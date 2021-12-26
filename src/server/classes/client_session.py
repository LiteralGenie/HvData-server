from hvpytils import HvSession

from multiprocessing.connection import Listener


class ClientSession(HvSession):
    RATE_LIMIT = 0

    authkey: str
    server_address: tuple[str, int]

    def __init__(self, server_address: tuple[str, int], authkey: str, **kwargs):
        super().__init__(**kwargs)
        self.server_address = server_address
        self.authkey = authkey

    def send(self, method: str, url: str, **kwargs):
        with Listener(self.server_address, authkey=self.authkey) as listener:
            with listener.accept() as conn:
                request = self.prepare_request(method, url, **kwargs)
                self.session.send(request)
                resp = conn.recv()
                
        return resp