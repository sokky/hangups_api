from django.db import models


class HangupsApiUser(models.Model):
    # 当システムに登録されるユーザのID
    user_id = models.CharField(max_length=200)
    # googleから提供されるreflesh_token：https://accounts.google.com/o/oauth2/token から取得
    token = models.CharField(max_length=200)
    # ユーザの名前など、識別させるためのフィールド
    memo = models.CharField(max_length=200)

