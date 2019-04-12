from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Wallpaper, Interior


class Interior(View):
    template_name = 'collections_app/interiors.html'
    interiors = Interior.objects.all()

    def get(self, request, *args, **kwargs):
        wallpapers = Wallpaper.objects.all()
        context = {'wallpapers': wallpapers, 'interiors': self.interiors}
        return render(request, self.template_name, context)

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.model.objects.all()
    #     return self.model.objects.exclude(Q(is_superuser=True) | Q(is_staff=True))