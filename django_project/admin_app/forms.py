from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
import re


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

    def clean_IFO(self):
        '''Определяем правило валидации поля IFO'''
        ifo = self.cleaned_data.get('IFO')
        ifo = str(ifo).split(' ')
        if len(ifo) != 3: # проверяет количество слов
            raise forms.ValidationError('Недостаточно данных!')
        else:
            for string in ifo:
                if not re.match('^[A-Za-zА-Яа-я]*$', string): # проверяем на соответствие регулярному выражению
                    raise forms.ValidationError('Текст должен содержать только буквы!')
        return self.cleaned_data


class EditForm(UserChangeForm):
    IFO = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'surname', 'email', 'username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.initial['IFO'] = '{} {} {}'.format(self.initial['first_name'],
        #                                         self.initial['last_name'],
        #                                         self.initial['surname'])
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()