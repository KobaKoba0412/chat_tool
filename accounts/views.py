from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views.generic import TemplateView
from .forms import UrlForm, LoginForm

class UrlFormView(View):
    def get(self, request, *args, **kwargs ):
        context = {
            "form": UrlForm(),
        }
        return render( request, 'accounts/UrlForm.html', context )

    def post(self, request, *args, **kwargs ):
        form = UrlForm(request.POST)
        if not form.is_valid():
            #バリデーションNG
            return render(request, 'accounts/UrlForm.html', {'form':form} )
        #form から　slack_url取得
        slack_url = form.cleaned_data["slack_url"]

        return redirect('/accounts/Login/')


sinin = UrlFormView.as_view()


class LogInView(AuthLoginView):
    form_class = LoginForm    
    template_name = 'accounts/login.html'

login = LogInView.as_view()


class SlackView(TemplateView):
    template_name = 'accounts/slack_main.html'

slack_main = SlackView.as_view()