from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model

from accounts.models import (
    WorkPlace,
)

User = get_user_model()


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        # 入力されたアドレスが仮登録されている場合、削除
        User.objects.filter(email=email, is_active=False).delete()
        return email


class TeamNameInputForm(forms.ModelForm):
    """チーム名の入力フォーム"""

    error_messages = {
        'registered_TeamName': ("It has already been registered."),
    }

    class Meta:
        model = WorkPlace
        fields = ('team_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_team_name(self):
        team_name = self.cleaned_data.get("team_name")

        if WorkPlace.objects.filter(team_name= team_name).exists():
            raise forms.ValidationError(
                self.error_messages['registered_TeamName'],
                code='registered_TeamName',
            )
        return team_name
            
class EmailInvitationForm(forms.ModelForm):
    """チームへの招待フォーム"""
    """仕組みはユーザ仮登録と同様の仕組み"""
    
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
