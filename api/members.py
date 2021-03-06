"""
Hangups_api_users に従って取得した会話情報を格納するオブジェクト
Hangups_api_users.user_idによって管理する。
"""


class _Members(object):

    clients = {}
    loops = {}

    def __init__(self):
        pass

    def get_client(self, id):
        return self.clients.get(id)

    def add_client(self, client, id):
        self.clients[id] = client

    def get_loop(self, id):
        return self.loops[id]

    def add_loop(self, loop, id):
        self.loops[id] = loop

Members = _Members()
