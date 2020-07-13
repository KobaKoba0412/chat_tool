from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)

from .models import Room

class CreateRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean(self):
        name = self.cleaned_data['name']

        # 同じRoom名は登録できないように制限
        if Room.objects.filter(name=name).exists():
            raise forms.ValidationError(
                "It has already been registered.",
            )
