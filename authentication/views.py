from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views import generic

from django.core.exceptions import ValidationError

User = get_user_model()

class Login(generic.TemplateView):
    """Login画面"""
    template_name = 'authentication/login.html'

class Logout(generic.TemplateView):
    """Logout画面"""
    template_name = 'authentication/logout.html'