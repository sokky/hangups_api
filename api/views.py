import asyncio

from django.http import HttpResponse, Http404
from django.views.generic import View
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from hangups import ChatMessageSegment, NetworkError

from api.models import HangupsApiUser
from api.serializers import UserSerializer, ConversationSerializer, MessageSerializer
from api.members import Members


class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
           return None

        return (user, None)



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class HangupsApiUsersView(View):
    def get(self, request):
        u = HangupsApiUser.objects.all()
        serializer = UserSerializer(u, many=True)
        return JSONResponse(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


class ConvListView(View):
    def get(self, request, user_id):
        m = Members
        client = m.get_client(user_id)
        if client:
            ret = ['conv_id']
            for conv in client._conv_list.get_all():
                ret.append(conv.id_)
            return HttpResponse(' '.join(ret))
        else:
            # userがいない場合
            raise Http404


class ConvListJson(View):
    def get(self, request, user_id):
        m = Members
        client = m.get_client(user_id)
        if client:
            serializer = ConversationSerializer(client._conv_list.get_all(), many=True)
            return JSONResponse(serializer.data)
        # userがいない場合
        raise Http404


class ConvJson(View):
    def get(self, request, user_id, conv_id):
        m = Members
        client = m.get_client(user_id)
        if client:
            conversation = client._conv_list.get(conv_id)
            if conversation:
                serializer = ConversationSerializer(conversation)
                return JSONResponse(serializer.data)

        # 該当するuser, conv_idがない場合
        raise Http404


class SendMessage(APIView):
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid()
        message = serializer.data

        m = Members
        client = m.get_client(message.get('user_id'))
        if client:
            conversation = client._conv_list.get(message.get('conv_id'))
            loop = m.get_loop(message.get('user_id'))
            if conversation:
                # testできたら移動
                text = message.get('message')
                image_file = None
                segments = ChatMessageSegment.from_str(text)

                asyncio.async(
                    conversation.send_message(segments, image_file=image_file),
                    loop=loop
                ).add_done_callback(self._on_message_sent)

                return HttpResponse("ok")

        # 該当するuser, conv_idがない場合
        raise Http404

    def get(self, request):
        m = Members
        client = m.get_client('test')
        if client:
            conversation = client._conv_list.get('UgyUUHcz02x_EFXA-Ht4AaABAagB_N-DBw')
            if conversation:
                # testできたら移動
                text = 'メッセージ送信テスト'
                image_file = None
                segments = ChatMessageSegment.from_str(text)

                loop = m.get_loop('test')
                asyncio.async(
                    conversation.send_message(segments, image_file=image_file),
                    loop=loop
                ).add_done_callback(self._on_message_sent)

                # 成功したら最新のconversationを返却
                # 若干遅延するからやめておきたい
                serializer = ConversationSerializer(conversation)
                return JSONResponse(serializer.data)

        # 該当するuser, conv_idがない場合
        raise Http404

    def _on_message_sent(self, future):
        """Handle showing an error if a message fails to send."""
        try:
            future.result()
        except NetworkError as e:
            print(e)


