from django.contrib import admin


from .models import HangupsApiUser, HangupsApiToken

admin.site.register(HangupsApiUser)
admin.site.register(HangupsApiToken)
