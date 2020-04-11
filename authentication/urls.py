from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('authentication/login', views.Login.as_view(), name='login'),
    path('authentication/logout', views.Logout.as_view(), name='logout'),
]
