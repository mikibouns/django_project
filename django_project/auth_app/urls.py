from django.urls import path
from . import views


app_name = 'auth_app'


urlpatterns = [
    path('signin', views.SignIn.as_view(), name='sign_in'),
    path('signout', views.sign_out, name='sign_out'),
]