from django.shortcuts import render, HttpResponseRedirect
from .forms import AuthenticationForm, UserRegisterForm
from django.contrib import auth
from django.urls import reverse


def authorization(request):
    login_form = AuthenticationForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/admin/')
        else:
            login_form = AuthenticationForm()
    content = {'login_form': login_form}
    return render(request, 'auth_app/authorisation.html', content)


def registration(request):
    reg_form = UserRegisterForm()
    template = "auth_app/register.html"
    context = {'reg_form': reg_form}
    return render(request, template, context)


def sign_in(request):
    return HttpResponseRedirect('/admin/')


def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))