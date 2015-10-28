from api.hangups import HangupsApi
from api.models import HangupsApiUser, HangupsApiToken
import threading
import tempfile

'''
serverがstartする時にあらかじめ呼び出すメソッドをここに定義する。
'''


def get_hangout_info():
    """Hangoutのアカウント情報から会話の履歴などを取得する"""
    users = HangupsApiUser.objects.all()
    for u in users:
        try:
            t = HangupsApiToken.objects.get(user_id=u.user_id)
            token = t.token
        except HangupsApiToken.DoesNotExist:
            token = HangupsApi.get_auth_token(u.token)
            if token:
                t = HangupsApiToken(
                    user_id=u.user_id,
                    token=token
                )
                t.save()

        _, path = tempfile.mkstemp(text=True)
        with open(path, 'w') as f:
            # tokenファイルの最後に改行はいれないこと
            f.write(token)
        t = threading.Thread(target=HangupsApi, args=(path, u.user_id))
        t.start()

    # TODO tempfileが残るので掃除をすること。
    # 再起動時が良いかも
