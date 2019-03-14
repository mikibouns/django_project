from django import forms
from django.contrib.auth import get_user_model
import re
from django.contrib.auth.forms import UserChangeForm


class CreateUserForm(forms.ModelForm):
    fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    username = forms.CharField(label='Имя пользователя')
    is_active = forms.CharField(label='Активный', widget=forms.CheckboxInput)
    is_staff = forms.CharField(label='Администратор', widget=forms.CheckboxInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('fio', 'email', 'username', 'is_active', 'is_staff', 'password')

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
            raise forms.ValidationError('Недостаточно данных!')
        else:
            for string in fio:
                if not re.match(r'^[A-Za-zА-Яа-я]*$', string): # проверяет на соответствие регулярному выражению
                    raise forms.ValidationError('Текст должен содержать только буквы!')
        fio_dict = {
            'first_name': fio[1],
            'lastname': fio[0],
            'surname': fio[2]
        }
        return fio_dict

    def clean_confirm_password(self):
        '''валидация пароля'''
        password = self.cleaned_data.get('password')
        conf_password = self.cleaned_data.get('confirm_password')
        if password or conf_password:
            if password != conf_password:
                raise forms.ValidationError('Пароли не совпадают!')
            else:
                if not re.match(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$', password):
                    raise forms.ValidationError('Пароль должен содержать не менее 8 симвоолов, буквы \
                    верхнего и нижнего регистра и цифры!')
        else:
            raise forms.ValidationError('Поле пароля пустое!')
        return self.cleaned_data['confirm_password']


class UpdateUserForm(UserChangeForm):
    fio = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    username = forms.CharField(label='Имя пользователя')
    is_active = forms.CharField(label='Активный', widget=forms.CheckboxInput)
    is_staff = forms.CharField(label='Администратор', widget=forms.CheckboxInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('fio', 'email', 'username', 'is_active', 'is_staff', 'password')

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
            raise forms.ValidationError('Недостаточно данных!')
        else:
            for string in fio:
                if not re.match(r'^[A-Za-zА-Яа-я]*$', string): # проверяет на соответствие регулярному выражению
                    raise forms.ValidationError('Текст должен содержать только буквы!')
        fio_dict = {
            'first_name': fio[1],
            'lastname': fio[0],
            'surname': fio[2]
        }
        return fio_dict

    def clean_confirm_password(self):
        '''валидация пароля'''
        password = self.cleaned_data.get('password')
        conf_password = self.cleaned_data.get('confirm_password')
        if password:
            if password != conf_password:
                raise forms.ValidationError('Пароли не совпадают!')
            else:
                if not re.match(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$', password):
                    raise forms.ValidationError('Пароль должен содержать не менее 8 симвоолов, буквы \
                    верхнего и нижнего регистра и цифры!')
        return self.cleaned_data['confirm_password']

    def delete_fields(self):
        del self.fields['is_active']
        del self.fields['is_staff']
