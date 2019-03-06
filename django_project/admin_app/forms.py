from django import forms
from django.contrib.auth import get_user_model
import re


class CreateUpdateUserForm(forms.Form):
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
        print(fio)
        fio = str(fio).split(' ')
        print(fio)
        if len(fio) != 3: # проверяет количество слов
            print('реально не равно')
            raise forms.ValidationError('Недостаточно данных!')
        else:
            for string in fio:
                if not re.match('^[A-Za-zА-Яа-я]*$', string): # проверяет на соответствие регулярному выражению
                    raise forms.ValidationError('Текст должен содержать только буквы!')
        return self.cleaned_data

    def clean_password(self):
        '''валидация пароля'''
        return self.cleaned_data