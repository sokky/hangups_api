from api.models import HangupsApiUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangupsApiUser
        fields = ('user_id', 'token', 'memo')
