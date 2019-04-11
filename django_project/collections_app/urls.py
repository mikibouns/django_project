from django.urls import path
from . import views

app_name = 'collections_app'


urlpatterns = [
    path('', views.Interior.as_view(), name='interior'),
]