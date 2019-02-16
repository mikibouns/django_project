from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class AuthenticationForm(forms.Form):
    '''Переопределяем форму аутентификации'''
    email = forms.CharField(
        label='E-mail',
        max_length=100,
        widget=forms.EmailInput(attrs={}),
        error_messages={'required': 'Укажите e-mail'})
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={}),)
        # error_messages={'required': 'Укажите пароль'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        self.current_user = None
        self.user_model = get_user_model()
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        '''Определяем правило валидации поля email'''
        email = self.cleaned_data.get('email')
        try:
            self.current_user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            raise forms.ValidationError('Указан не верный e-mail!')
        return self.cleaned_data

    def clean_password(self):
        '''Определяем правило валидации поля password'''
        passwd = str(self.cleaned_data.get('password'))
        if len(passwd) < 8:
            raise forms.ValidationError('Пароль должен быть не менее 8 символов!')
        if self.current_user:
            if not self.current_user.check_password(passwd):
                raise forms.ValidationError('Указан не верный пароль!')
        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    FIO = forms.CharField(label='ФИО')
    phone = forms.CharField(label='Телефон')
    www = forms.CharField(label='Сайт отеля')
    vacations = forms.CharField(label='Количество номеров')
    pms = forms.Select(label='Какую PMS использует', )


    class Meta:
        model = get_user_model()
        fields = ('FIO', 'phone', 'email', 'www', 'vacations', 'pms', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


# class UserEditForm(UserChangeForm):
#     class Meta:
#         model = HLUsers
#         fields = ('username', 'first_name', 'email', 'au_age', 'au_avatar',
#                   'password')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''
#             if field_name == 'password':
#                 field.widget = forms.HiddenInput()
#
#     def clean_age(self):
#         data = self.cleaned_data['age']
#         if data < 18:
#             raise forms.ValidationError("You are too young!")
#         return data