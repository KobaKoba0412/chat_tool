# chat/routing.py
from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'chat_room/(?P<room_name>\w+)/$', consumer.ChatConsumer),
]