from django.shortcuts import render, HttpResponseRedirect
from .forms import AuthenticationForm, RegisterForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import EmailMessage
import smtplib
from django_project.settings import EMAIL_HOST_USER
from django.views import View


class SignIn(View):
    initial = {'key': 'value'}
    form_class = AuthenticationForm
    template = 'auth_app/authorisation.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template, {'login_form': form})

    def post(self, request,*args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=email, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('auth:sign_in'))
            else:
                form = AuthenticationForm()

        return render(request, self.template, {'login_form': form})


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:sign_in'))


class Registration(View):
    initial = {'key': 'value'}
    form_class = RegisterForm
    template = 'auth_app/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template, {'reg_form': form})

    def post(self, request, *args, **kwargs):
        error = ''
        form = self.form_class(data=request.POST)
        if form.is_valid():
            pms = request.POST.get('pms', None)
            message = self.create_letter(request, pms)
            sending_result = self.send_letter(message)
            if not sending_result:
                return HttpResponseRedirect(reverse('main:welcome'))
            else:
                error = sending_result
        return render(request, self.template, {'reg_form': form, 'send_mail_error': error})

    def create_letter(self, request, pms):
        '''создание тела письма'''
        if pms == 'another': # если выбрана "другая" pms, присвоить значение из поля "another_pms"
            pms = request.POST.get('another_pms', None)
        message = '''
                ФИО: {}, 
                Телефон: {}, 
                E-mail: {},
                Сайт отеля: {},
                Количество номеров: {},
                PMS: {},
                Часовой пояс: {}
                '''.format(request.POST.get('FIO', None),
                           request.POST.get('phone', None),
                           request.POST.get('email', None),
                           request.POST.get('www', None),
                           request.POST.get('vacations', None),
                           pms,
                           request.POST.get('timeZ', None), )
        return message

    def send_letter(self, message):
        '''отправка письма заявки'''
        try:
            msg = EmailMessage(
                subject=u'Тема письма',
                body=message,
                from_email=EMAIL_HOST_USER,
                to=('igor.matiek@yandex.ru',)
            )
            msg.send()
            return None
        except smtplib.SMTPException as e:
            send_mail_error = '''Письмо небыло доставлено, попробуйте с нами связаться по
                                телефону 8(800)888-88-88 чтобы оставить заявку'''

            print(e)
            return send_mail_error