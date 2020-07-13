# coding: utf-8
import os
import django
from channels.routing import get_default_application

#print("asgi.py().SETTING_FILE={}".format(os.environ.get('SETTING_FILE','NULL')))
#本番環境
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
#docker-compose ymlファイルに依存
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('SETTING_FILE','config.settings.production'))
django.setup()
application = get_default_application()