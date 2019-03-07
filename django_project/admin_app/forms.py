from django import forms
from django.contrib.auth import get_user_model
import re


class CreateUserForm(forms.Form):
    fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    username = forms.CharField(label='Имя пользователя')
    is_active = forms.CharField(label='Активный', widget=forms.CheckboxInput)
    is_staff = forms.CharField(label='Администратор', widget=forms.CheckboxInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_active' or field_name == 'is_staff':
                field.widget.attrs['class'] = 'form-check-input'
            field.required = False
            field.help_text = ''

    def clean_fio(self):
        '''Определяем правило валидации поля FIO'''
        fio = self.cleaned_data.get('fio')
        fio = str(fio).split(' ')
        if len(fio) != 3: # проверяет количество слов
            print('реально не равно')
            raise forms.ValidationError('Недостаточно данных!')
        else:
            for string in fio:
                if not re.match(r'^[A-Za-zА-Яа-я]*$', string): # проверяет на соответствие регулярному выражению
                    raise forms.ValidationError('Текст должен содержать только буквы!')
        return self.cleaned_data

    def clean_username(self):
        '''валидация пользователя, существует в БД или нет'''
        user = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=user).exists():
            raise forms.ValidationError('Пользователь {} уже существует!'.format(user))
        return self.cleaned_data

    def clean_confirm_password(self):
        '''валидация пароля'''
        password = self.cleaned_data.get('password')
        conf_password = self.cleaned_data.get('confirm_password')
        if password != conf_password:
            raise forms.ValidationError('Пароли не совпадают!')
        else:
            if not re.match(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$', password):
                raise forms.ValidationError('Пароль должен содержать не менее 8 симвоолов, буквы \
                верхнего и нижнего регистра и цифры!')
        return self.cleaned_data


class UpdateUserForm(CreateUserForm):
    def clean_username(self):
        '''переопределяем валидацию username. чтобы не ругался на существующего пользователя'''
        return self.cleaned_data
