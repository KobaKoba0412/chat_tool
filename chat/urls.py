from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>', views.chat, name='chat_room'),
    path('room/', views.room, name='room'),
]
