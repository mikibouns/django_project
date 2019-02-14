from django.db import models
from django.contrib.auth.models import AbstractUser


class HLUsers(AbstractUser):
    '''Пользователи'''
    lastname = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    phone = models.CharField(max_length=18)
    timeZ = models.CharField(max_length=128)
    params = models.TextField()

    def __str__(self):
        return self.username























