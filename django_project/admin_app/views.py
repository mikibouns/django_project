from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class AdminPanel(TemplateView):
    template_name = 'admin_app/admin_panel.html'
