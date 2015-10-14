from api.models import HangupsApiUser
from rest_framework import serializers


class HangupsConvEventField(serializers.Field):
    """ConversationのEvent一覧をシリアライズするためのクラス"""
    def to_representation(self, obj):
        return obj.id_

    def to_internal_value(self, data):
        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangupsApiUser
        # tokenは隠す
        fields = ('user_id', 'memo')


class HangupsUserIDSerializer(serializers.Serializer):
    chat_id = serializers.CharField()
    gaia_id = serializers.CharField()


class HangupsUserSerializer(serializers.Serializer):
    id_ = HangupsUserIDSerializer()
    full_name = serializers.CharField()
    first_name = serializers.CharField()
    photo_url = serializers.URLField()
    emails = serializers.ListField(child=serializers.EmailField())
    is_self = serializers.BooleanField()


class ConversationSerializer(serializers.Serializer):
    id_ = serializers.CharField()
    users = HangupsUserSerializer(many=True)
    name = serializers.CharField()
    last_modified = serializers.DateTimeField()
    latest_read_timestamp = serializers.DateTimeField()
    events = serializers.ListField(child=HangupsConvEventField())
