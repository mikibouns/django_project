from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class CreateForm(UserCreationForm):
    IFO = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))

    class Meta:
        model = get_user_model()
        fields = ('IFO', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class EditForm(UserChangeForm):
    IFO = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))

    class Meta:
        model = get_user_model()
        fields = ('IFO', 'email', 'username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()