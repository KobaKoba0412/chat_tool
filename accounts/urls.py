from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('URL_FORM/', views.UrlFormView.as_view(), name="UrlForm"),
    path('Login/', views.LogInView.as_view(), name="LogIn"),
    path('Slak_main/', views.SlackView.as_view(), name="Slack"),
]
