from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'register'

urlpatterns = [
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/temporary_done', views.TemporaryDone.as_view(), name='temporary_done'),  #仮登録完了
    path('user_create/join_done/<token>/', views.JoinDone.as_view(), name='join_done'),
]
