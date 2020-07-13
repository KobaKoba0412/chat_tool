from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views.generic import TemplateView
from .forms import UrlForm, LoginForm
from django.contrib.auth import logout

class LogInView(AuthLoginView):
    form_class = LoginForm    
    template_name = 'accounts/login.html'

login = LogInView.as_view()


class LogOutView(View):
    def get(self, request, *args, **kwargs ):
        logout(request)
        # Redirect to a success page.
        return redirect('accounts:LogIn')

