from django.conf.urls import url, include
from api.views import user_list, login


urlpatterns = [
    url(r'^users/$', user_list),
    url(r'^login/$', login)
]
