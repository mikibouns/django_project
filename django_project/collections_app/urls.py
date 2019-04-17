from django.urls import path
from . import views

app_name = 'collections_app'


urlpatterns = [
    path('', views.CollectionView.as_view(), name='collection'),
    path('<str:name>', views.WallpaperView.as_view(), name='wallpaper'),
    path('<str:name>/interiors', views.InteriorView.as_view(), name='interior'),
]