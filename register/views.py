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
from .forms import (
    LoginForm, UserCreateForm,TeamNameInputForm
)


User = get_user_model()
...
...
...
class UserCreate(generic.CreateView):

     """ユーザー仮登録"""
     template_name = 'register/user_create.html'
     form_class = UserCreateForm

     def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk), #プライマリーキー⇒tokenへ変換
            'user': user,
        }

        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('register:temporary_done')


class TemporaryDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/temporary_done.html'

class TeamNameInput(View):
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24) 
    """チーム名の入力"""
    def get(self, request, *args, **kwargs ):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')   #token 取得
        try:
            #token⇒プライマリーキーへ変換
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                #プライマリーキーからユーザ情報を取得
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ引き続きチーム名などの入力を行う。
                    context ={"form": TeamNameInputForm(),
                              "user":user_pk,#user情報はhidden情報で引き継ぐ
                    }
                    
                    return render( request, 'register/input_TeamName.html', context )

        #トークンの認証失敗
        return HttpResponseBadRequest()


    def post(self, request, *args, **kwargs ):
        form = TeamNameInputForm(request.POST)
        if not form.is_valid():
            #バリデーションNG
            return render(request, 'register/input_TeamName.html', {'form':form} )

        user_pk = form.data["user"]
        try:
            #プライマリーキーからユーザ情報を取得
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            user.is_active = True #本登録
            user.save()

            #form入力した内容取得、
            team = form.save(commit=False)
            team.work_place_url = team.name + 'url' #とりあえず適当
            team.members = user # 登録者をチームメンバー最初の人に登録  
            form.save()

            return redirect('register:user_create_complete')

team_name = TeamNameInput.as_view()


class UserCreateComplete(generic.TemplateView):
    """ユーザー本登録＆メンバーの招待画面(任意、後で登録可能)"""
    template_name = 'register/user_complete_and_invitation.html'
    form_class = EmailInvitationForm

    def form_valid(self, form):
    """　招待メールの発行　"""
    current_site = get_current_site(self.request)
    domain = current_site.domain
    context = {
        'protocol': self.request.scheme,
        'domain': domain,
        'token': dumps(user.pk), #プライマリーキー⇒tokenへ変換
        'user': user,
    }

    subject = render_to_string('register/mail_template/create/subject.txt', context)
    message = render_to_string('register/mail_template/create/message.txt', context)

    user.email_user(subject, message)
    return redirect('register:temporary_done')

    