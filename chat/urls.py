from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.ChatMain.as_view(), name='chat_main'),
]
