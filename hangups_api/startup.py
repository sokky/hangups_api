from api.hangups import HangupsApi
from api.models import HangupsApiUser
import threading
import tempfile

'''
serverがstartする時にあらかじめ呼び出すメソッドをここに定義する。
'''


def get_hangout_info():
    """Hangoutのアカウント情報から会話の履歴などを取得する"""
    users = HangupsApiUser.objects.all()
    for u in users:
        _, path = tempfile.mkstemp(text=True)
        with open(path, 'w') as f:
            # tokenファイルの最後に改行はいれないこと
            f.write(u.token)
        t = threading.Thread(target=HangupsApi, args=(path,))
        t.start()

    # TODO tempfileが残るので掃除をすること。
    # 再起動時が良いかも
