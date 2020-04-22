from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate,login
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
    UserCreateForm,
)
from .backends import (HashedPasswordAuthBackend,)

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

"""
class TeamNameInput(View):
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24) 
    
    def get(self, request, *args, **kwargs ):

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
                user.is_active = True #本登録
                user.save()

                #　Loginも同時に行う。 
                login(request, user)
               
                #　チームの登録
                team = form.save(commit=False)
                team.name = team.team_name #同じでいいや
                team.work_place_url = team.team_name + '.url' #とりあえず適当
                form.save()

                # ユーザとチームの紐づけ
                WorkPlacePersonRelation.objects.create(workPlace= team,User = user, login_status = 0)

                return redirect('register:create_complete_Invitation')
        
        #トークンの認証失敗
        return HttpResponseBadRequest()

team_name = TeamNameInput.as_view()

"""
"""
class UserCreateCompleteAndInvitation(generic.CreateView):

    template_name = 'register/user_complete_and_invitation.html'
    form_class = EmailInvitationForm

    def post(self, request, *args, **kwargs):

        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):

        user = form.save(commit=False)
        user.is_active = False #仮登録と同様のステータスにする
        user.save()

        invite = Invitation.create(user.email, inviter=request.user)
        invite.send_invitation(request)
        return redirect('register:invitation_done')

"""

"""
class InvitationDone(generic.TemplateView):
    template_name = 'register/invitation_done.html'
"""

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
                user.is_active = True #本登録
                user.save()

                context ={"guest_email":user.email, #表示用email情報
                         "user":user_pk,            #user情報はhidden情報で引き継ぐ
                } 
                
                return render( request, 'register/join_done.html', context )
    
        #トークンの認証失敗
        return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs ):

        # ログイン
        user = User.objects.get(pk =request.POST['user'])
        auth = HashedPasswordAuthBackend()
        auth.authenticate(request=request)
        login(request, user)

        return redirect('chat:chat_main')

join_done = JoinDone.as_view()

"""
class FrendsPasswordRegister(generic.CreateView):
    
    template_name = 'register/frends_pw_reg.html'
    form_class = FrendsPwRegForm

    def get(self, request, *args, **kwargs ):
        self.frend_email = unstash_verified_email(request)
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['frends_email'] = self.frend_email
        return ctx

    def unstash_verified_email(self, request):
        # session情報　から ユーザEmail情報取得
        ret = request.session.get('account_verified_email')
        request.session['account_verified_email'] = None
        return ret

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return redirect('register:temporary_done')

frends_pw_reg = FrendsPasswordRegister.as_view()

"""