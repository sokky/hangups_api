from django.conf.urls import url, include
from api.views import HangupsApiUsersView, ConvListJson, ConvListView, ConvJson


urlpatterns = [
    url(r'^hangups_api_users/$', HangupsApiUsersView.as_view()),
    url(r'^hangups_api_users/(?P<user_id>\w+)/$', ConvListView.as_view()),
    url(r'^hangups_api_users/(?P<user_id>\w+)\.json', ConvListJson.as_view()),
    url(r'^hangups_api_users/(?P<user_id>\w+)/(?P<conv_id>\w+)\.json', ConvJson.as_view()),
]
