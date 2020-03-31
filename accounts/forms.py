from django import forms
from django.contrib.auth.forms import UsernameField

from .models import WorkPlace
from django.db.models import ObjectDoesNotExist

from django.contrib.auth.forms import AuthenticationForm

class UrlForm(forms.Form):
    """Slack_URL入力用画 ⾯  のフォーム"""
    slack_url = forms.CharField(
        label='',
        max_length=100,  #一応このぐらいでいいか
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'placeholder': "your-workspace-url",
            }),
    )

    def clean_slack_url(self):
        #入力値はcleaned_data から取得
        slack_url = self.cleaned_data['slack_url']
        #データベース上に入力されたurlがあるか検索
        try:
            registared_url = WorkPlace.objects.get(work_place_url = slack_url)
        except ObjectDoesNotExist:
            raise forms.ValidationError("ワークスペースが見つかりませんでした。")
        return slack_url

    def clean(self):
        #特にチェック無し
        pass





class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる