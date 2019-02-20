from django.shortcuts import render, HttpResponseRedirect
from .forms import AuthenticationForm, RegisterForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import EmailMessage
import smtplib
from django_project.settings import EMAIL_HOST_USER


def sign_in(request):
    login_form = AuthenticationForm()
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=email, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('auth:sign_in'))
            else:
                login_form = AuthenticationForm()
    content = {'login_form': login_form}
    return render(request, 'auth_app/authorisation.html', content)


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:sign_in'))


def registration(request):
    reg_form = RegisterForm()
    send_mail_error = ''
    if request.method == 'POST':
        reg_form = RegisterForm(data=request.POST)
        if reg_form.is_valid():
            pms = request.POST.get('pms', None)
            if pms == 'another':
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
                       request.POST.get('timeZ', None),)
            try:
                msg = EmailMessage(
                    subject=u'Тема письма',
                    body=message,
                    from_email=EMAIL_HOST_USER,
                    to=('igor.matiek@yandex.ru',)
                )
                msg.send()
                return HttpResponseRedirect(reverse('main'))
            except smtplib.SMTPException as e:
                send_mail_error = '''Письмо небыло доставлено, попробуйте с нами связаться по
                            телефону 8(800)888-88-88 чтобы оставить заявку'''
                print(e)
    template = "auth_app/register.html"
    context = {'reg_form': reg_form,
               'send_mail_error': send_mail_error}
    return render(request, template, context)
