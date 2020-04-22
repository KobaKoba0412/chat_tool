from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model

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

"""
class TeamNameInputForm(forms.ModelForm):
    
    error_messages = {
        'registered_TeamName': ("It has already been registered."),
    }

    class Meta:
        model = WorkPlace
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data.get("team_name")

        # 同じチーム名は登録できないように制限
        if WorkPlace.objects.filter(name= name).exists():
            raise forms.ValidationError(
                self.error_messages['registered_TeamName'],
                code='registered_TeamName',
            )
        return name
"""

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

class FrendsPwRegForm(UserCreationForm):
    """友達登録用フォーム（Password Only）"""

    class Meta:
        model = User
        fields = () # Password 以外不要

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    