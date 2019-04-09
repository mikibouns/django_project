from django.shortcuts import render
from django.views.generic import TemplateView

class Welcome(TemplateView):
    template_name = 'main_app/welcome.html'


class TestImg(TemplateView):
    template_name = 'main_app/image.html'