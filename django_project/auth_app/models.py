from django.db import models
from django.contrib.auth.models import AbstractUser


class HLUsers(AbstractUser):
    '''Пользователи'''
    lastname = models.CharField(max_length=256, blank=True, null=True)
    surname = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=18, blank=True, null=True)
    timeZ = models.CharField(max_length=128, blank=True, null=True)
    params = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username























