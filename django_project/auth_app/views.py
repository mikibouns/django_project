from django.shortcuts import render


def authorization(request):
    template = "auth_app/authorisation.html"
    context = {}
    return render(request, template, context)


def registration(request):
    template = "auth_app/register.html"
    context = {}
    return render(request, template, context)


def sign_in():
    return None


def sign_out():
    return None