from django.shortcuts import render, HttpResponseRedirect
from .forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
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
    reg_form = UserCreationForm(data=request.POST)
    if request.method == 'POST' and reg_form.is_valid():
        message = '''
        ФИО: {}, 
        Телефон: {}, 
        E-mail: {},
        Сайт отеля: {},
        Количество номеров: {},
        PMS: {},
        Часлвлй пояс: {}
        '''.format(request.POST.get('FIO', None),
                   request.POST.get('phone', None),
                   request.POST.get('email', None),
                   request.POST.get('www', None),
                   request.POST.get('vacations', None),
                   request.POST.get('pms', None),
                   request.POST.get('timeZ', None),)
        try:
            send_mail(
                'Заявка клиента',
                message,
                EMAIL_HOST_USER,
                ['igor.matiek@yandex.ru'],
                fail_silently=False,
            )
        except smtplib.SMTPException as error:

            print(error)
    template = "auth_app/register.html"
    context = {'reg_form': reg_form}
    return render(request, template, context)


def sign_in(request):
    return HttpResponseRedirect('/admin/')


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:auth'))