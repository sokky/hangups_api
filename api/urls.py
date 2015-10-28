from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from api.views import HangupsApiUsersView, ConvListJson, ConvListView, ConvJson, SendMessage


urlpatterns = [
    url(r'^hangups_api_users/$', HangupsApiUsersView.as_view()),
    url(r'^hangups_api_users/(?P<user_id>\w+)/$', ConvListView.as_view()),
    url(r'^hangups_api_users/(?P<user_id>\w+)\.json', ConvListJson.as_view()),
    url(r'^hangups_api_users/(?P<user_id>\w+)/(?P<conv_id>\w+)\.json', ConvJson.as_view()),
    url(r'^hangups_api_users/send', csrf_exempt(SendMessage.as_view())),
]
