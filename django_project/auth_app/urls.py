from django.urls import path, include
from . import views


app_name = 'auth_app'


urlpatterns = [
    path('', views.authorization, name='auth'),
    path('register/', views.registration, name='register'),
]