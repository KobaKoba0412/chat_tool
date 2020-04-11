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
    LoginForm, UserCreateForm,TeamNameInputForm, EmailInvitationForm,
)

from accounts.models import (
    WorkPlace,WorkPlacePersonRelation,
)

from django.core.exceptions import ValidationError
from invitations.utils import get_invitation_model

User = get_user_model()
Invitation = get_invitation_model()
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
                              "user":user_pk,        #user情報はhidden情報で引き継ぐ
                    }
                    
                    return render( request,'register/input_TeamName.html', context )

        #トークンの認証失敗
        return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs ):
        form = TeamNameInputForm(request.POST)
        if not form.is_valid():
            #バリデーションNG
            return render(request,'register/input_TeamName.html', {'form':form} )

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

            team.name = team.team_name #同じでいいや
            team.work_place_url = team.team_name + '.url' #とりあえず適当
            form.save()

            WorkPlacePersonRelation.objects.create(workPlace= team,User = user, login_status = 0)

            return redirect('register:create_complete_Invitation')

team_name = TeamNameInput.as_view()


class UserCreateCompleteAndInvitation(generic.CreateView):
    """ユーザー本登録＆メンバーの招待画面(任意、後で登録可能)"""
    template_name = 'register/user_complete_and_invitation.html'
    form_class = EmailInvitationForm

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        """　招待メールの発行　"""
        user = form.save(commit=False)
        user.is_active = False #仮登録と同様のステータスにする
        user.save()

        invite = Invitation.create('imagista2@outlook.jp', inviter=request.user)
        invite.send_invitation(request)
        return redirect('register:invitation_done')
        
"""
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk), #プライマリーキー⇒tokenへ変換
            'user': user,
        }

        subject = render_to_string('register/mail_template/invitation/subject.txt', context)
        message = render_to_string('register/mail_template/invitation/message.txt', context)

        user.email_user(subject, message)
"""


class InvitationDone(generic.TemplateView):
    """友達を招待しました。"""
    template_name = 'register/invitation_done.html'

class JoinDone(View):
    """参加しました。"""
    template_name = 'register/join_done.html'

    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24) 
    
    def get(self, request, *args, **kwargs ):
        """tokenが正しければ友達の本登録完了."""
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
                    context ={"guest_email":user.email,  #表示用email情報
                              "user":user_pk,             #user情報はhidden情報で引き継ぐ
                    }
                    
                    return render( request, 'register:join_done', context )
        
        #トークンの認証失敗
        return HttpResponseBadRequest()

join_done = JoinDone.as_view()