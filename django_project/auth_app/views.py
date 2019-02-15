from django.shortcuts import render, HttpResponseRedirect
from .forms import UserLoginForm
from django.contrib import auth
from django.urls import reverse


def authorization(request):
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('admin'))

    content = {'login_form': login_form}
    return render(request, 'auth_app/authorisation.html', content)


def registration(request):
    template = "auth_app/register.html"
    context = {}
    return render(request, template, context)


def sign_in(request):
    return None


def sign_out():
    return None