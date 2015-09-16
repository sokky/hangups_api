"""
WSGI config for hangups_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hangups_api.settings")


application = get_wsgi_application()

import hangups_api.startup as startup
# hangout情報の取得
startup.get_hangout_info()

