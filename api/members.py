class _Members(object):

    clients = {}

    def __init__(self):
        pass

    def get_client(self):
        return self.clients.get("test")

    def add_client(self, client):
        self.clients["test"] = client

Members = _Members()
