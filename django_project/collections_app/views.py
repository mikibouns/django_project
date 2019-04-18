from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Wallpaper, Interior, Collection


class InteriorView(View):
    template_name = 'collections_app/interiors.html'
    interiors = Interior.objects.all()
    collections = Collection.objects.all()

    def get(self, request, *args, **kwargs):
        wallpapers = Wallpaper.objects.all()
        context = {'wallpapers': wallpapers,
                   'interiors': self.interiors,
                   'collections': self.collections}
        return render(request, self.template_name, context)

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return self.model.objects.all()
    #     return self.model.objects.exclude(Q(is_superuser=True) | Q(is_staff=True))


class CollectionView(TemplateView):
    template_name = 'collections_app/collections.html'

    def get(self, request, *args, **kwargs):
        collections = Collection.objects.all()
        context = {'collections': collections}
        return render(request, self.template_name, context)


class WallpaperView(View):
    template_name = 'collections_app/wallpapers.html'

    def get(self, request, name, *args, **kwargs):
        collection = Collection.objects.filter(name=name)
        context = {'current_collection': name, 'collection': collection}
        return render(request, self.template_name, context)