from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import HangupsApiUser
from api.serializers import UserSerializer
from api.members import Members


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def user_list(request):
    """

    """
    if request.method == 'GET':
        u = HangupsApiUser.objects.all()
        serializer = UserSerializer(u, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def login(request):
    """
    :param request:
    :return:
    """
    m = Members
    print([x.full_name for x in m.get_client()._user_list.get_all()])
    return JSONResponse({"test": "aaa"})



