from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
import re


class CreateUpdateUserForm(forms.Form):
    FIO = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('FIO', 'email', 'username', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_FIO(self):
        '''Определяем правило валидации поля IFO'''
        fio = self.cleaned_data.get('FIO')
        fio = str(fio).split(' ')
        if len(fio) != 3: # проверяет количество слов
            raise forms.ValidationError('Недостаточно данных!')
        else:
            for string in fio:
                if not re.match('^[A-Za-zА-Яа-я]*$', string): # проверяет на соответствие регулярному выражению
                    raise forms.ValidationError('Текст должен содержать только буквы!')
        return self.cleaned_data