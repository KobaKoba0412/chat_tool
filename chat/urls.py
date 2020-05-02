from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'chat'

urlpatterns = [
    path('', login_required(views.index.as_view()), name='index'),
    path('<str:room_name>', login_required(views.chat.as_view()), name='chat_room'),
    path('room/', login_required(views.room.as_view()), name='room'),
]
