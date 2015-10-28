import sys
import asyncio
import hangups
import hangups.conversation_event
import hangups.auth
import api.members
import tempfile


class HangupsApi(object):
    """Hangupに接続、イベント等を行うクラス"""

    def __init__(self, refresh_token_path, id):

        self._client = None
        self._conv_list = None
        self._user_list = None
        self._id = id

        try:
            cookies = hangups.auth.get_auth_stdin(refresh_token_path)
        except hangups.GoogleAuthError as e:
            sys.exit('Login failed ({})'.format(e))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self._client = hangups.Client(cookies)
        self._client.on_connect.add_observer(self._on_connect)

        #asyncio.async(
        #        self._client.connect()
        #    ).add_done_callback(lambda future: future.result())
        # loop = asyncio.get_event_loop()
        loop.run_until_complete(self._client.connect())

    @asyncio.coroutine
    def _on_connect(self, initial_data):
        """Handle connecting for the first time"""
        # print('Connected!')
        self._retry = 0
        self._user_list = yield from hangups.build_user_list(
            self._client,
            initial_data
        )
        self._conv_list = hangups.ConversationList(
            self._client,
            initial_data.conversation_states,
            self._user_list,
            initial_data.sync_timestamp
        )
        self._conv_list.on_event.add_observer(self._on_event)

        m = api.members.Members
        m.add_client(self, self._id)
        loop = asyncio.get_event_loop()
        m.add_loop(loop, self._id)

    def _on_event(self, conv_event):
        """Open conversation tab for new messages when they arrive."""
        conv = self._conv_list.get(conv_event.conversation_id)
        user = conv.get_user(conv_event.user_id)

    def _on_quit(self):
        """Handle the user quitting the application."""
        future = asyncio.async(self._client.disconnect())
        future.add_done_callback(lambda future: future.result())

    @staticmethod
    def get_auth_token(reflesh_token):
        """reflesh_tokenから内部で利用する恒常的なtokenへ変換する
        reflesh_tokenは一度しか使えないため注意"""
        def get_code_f():
            print("token", reflesh_token)
            return reflesh_token

        _, path = tempfile.mkstemp(text=True)
        try:
            hangups.auth._auth_with_code(get_code_f, path)
        except hangups.GoogleAuthError as e:
            print(e)
        with open(path) as f:
            token = f.read()
        return token
