from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('Login/', views.LogInView.as_view(), name="LogIn"),
]
