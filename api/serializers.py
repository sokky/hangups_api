from hangups import conversation_event
from api.models import HangupsApiUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangupsApiUser
        # tokenは隠す
        fields = ('user_id', 'memo')


class MessageSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    conv_id = serializers.CharField()
    message = serializers.CharField()


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


class HangupsConvEventSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        ret = {}

        # 共通部
        ret['id_'] = obj.id_
        ret['conversation_id'] = obj.conversation_id
        ret['user_id'] = {
            'chat_id': obj.user_id.chat_id,
            'gaia_id': obj.user_id.gaia_id
        }
        ret['timestamp'] = obj.timestamp

        # イベントによって変える部分
        if isinstance(obj, conversation_event.ChatMessageEvent):
            segments = []
            for e in obj.segments:
                segments.append({
                    'text': e.text,
                    'is_bold': e.is_bold,
                    'is_italic': e.is_italic,
                    'is_strikethrough': e.is_strikethrough,
                    'is_underline': e.is_underline,
                    'link_target': e.link_target
                })

            ret['event'] = {
                'obj': 'ChatMessageEvent',
                'text': obj.text,
                'segment': segments,
                'attachments': obj.attachments
            }
        elif isinstance(obj, conversation_event.RenameEvent):
            ret['event'] = {
                'obj': 'RenameEvent',
                'new_name': obj.new_name,
                'old_name': obj.old_name,
            }
        elif isinstance(obj, conversation_event.MembershipChangeEvent):
            ids = []
            for i in obj.participant_ids:
                ids.append({
                    'chat_id': i.chat_id,
                    'gaia_id': i.gaia_id,
                })
            ret['event'] = {
                'obj': 'RenameEvent',
                'type': obj.type_,
                'participant_ids': ids,
            }
        else:
            # それ以外の場合はどんなイベントか不明
            ret['event'] = {
                'obj': 'ConversationEvent',
            }
        return ret


class ConversationSerializer(serializers.Serializer):
    id_ = serializers.CharField()
    users = HangupsUserSerializer(many=True)
    name = serializers.CharField()
    last_modified = serializers.DateTimeField()
    latest_read_timestamp = serializers.DateTimeField()
    events = HangupsConvEventSerializer(many=True)
