import pytz
import tzlocal
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
        error_messages={'required': ''})
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={}),
        error_messages={'required': ''})

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        self.current_user = None
        self.user_model = get_user_model()
        super().__init__(*args, **kwargs)
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


class UserCreationForm(forms.Form):
    pms_list = (('Fidelio_PMS', 'Fidelio PMS'),
                ('Opera_PMS', 'Opera PMS'),
                ('1C_Hotel', '1C Hotel'),
                ('Logus_HMS', 'Logus HMS'),
                ('Edelweiss', 'Edelweiss'),
                ('Travelline_Web_PMS', 'Travelline Web PMS'),
                ('Bnovo_PMS', 'Bnovo PMS'),
                ('Shelter', 'Shelter'),
                ('another', 'Другая'))
    FIO = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'id': 'phone'}))
    email = forms.CharField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'id': 'email'}))
    www = forms.CharField(label='Сайт отеля', widget=forms.URLInput(attrs={'required': False}))
    vacations = forms.CharField(label='Количество номеров', widget=forms.TextInput(attrs={'required': False}))
    pms = forms.CharField(label='Какую PMS использует',
                          widget=forms.Select(choices=pms_list, attrs={'id': 'pms'}))
    another_pms = forms.CharField(label='Другая PMS', widget=forms.TextInput(attrs={'id': 'another_pms',
                                                                                    'required': False}))
    timeZ = forms.CharField(label='Часовой пояс',
                            widget=forms.Select(choices=((tz, tz) for tz in pytz.all_timezones),
                                                attrs={'required': False}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['timeZ'] = tzlocal.get_localzone()
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