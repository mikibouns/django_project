from django.shortcuts import render, HttpResponseRedirect
from .forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import EmailMessage
import smtplib
from django_project.settings import EMAIL_HOST_USER


def authorization(request):
    login_form = AuthenticationForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('auth:auth'))
        else:
            login_form = AuthenticationForm()
    content = {'login_form': login_form}
    return render(request, 'auth_app/authorisation.html', content)


def registration(request):
    send_mail_error = ''
    reg_form = UserCreationForm()
    if request.method == 'POST':
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
                to=('igor.matiek@yandex.ru',),
                # headers={'From': 'email_from@me.com'}
            )
            msg.send()
        except smtplib.SMTPException as e:
            send_mail_error = '''Письмо небыло доставлено, попробуйте с нами связаться по
                        телефону 8(800)888-88-88 чтобы оставить заявку'''
            print(e)
    template = "auth_app/register.html"
    context = {'reg_form': reg_form,
               'send_mail_error': send_mail_error}
    return render(request, template, context)


def sign_in(request):
    return HttpResponseRedirect('/admin/')


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:auth'))