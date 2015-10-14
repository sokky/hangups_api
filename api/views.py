from django.http import HttpResponse, Http404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import HangupsApiUser
from api.serializers import UserSerializer, ConversationSerializer
from api.members import Members


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
            return HttpResponse("hoge")
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
        else:
            # userがいない場合
            raise Http404


@csrf_exempt
def login(request):
    """
    :param request:
    :return:
    """
    m = Members
    print([x.full_name for x in m.get_client()._user_list.get_all()])
    return JSONResponse({"test": "aaa"})



