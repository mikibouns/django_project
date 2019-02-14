from django.urls import path, include
from . import views


app_name = 'auth_app'


urlpatterns = [
    path('', views.authorization, name='auth'),
    path('register/', views.registration, name='register'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),
]