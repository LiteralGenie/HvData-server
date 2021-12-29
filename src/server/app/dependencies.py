from classes.client_session import ClientSession


# We dont need to call session.login() because this is basically a proxy for the real session (which is already logged in)
session = ClientSession()

