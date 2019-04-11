from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import Wallpaper


class Interior(ListView):
    model = Wallpaper
    template_name = 'collections_app/interiors.html'

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.model.objects.all()
    #     return self.model.objects.exclude(Q(is_superuser=True) | Q(is_staff=True))