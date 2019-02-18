from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


class Places(MPTTModel):
    '''Топонимы'''
    title = models.CharField(max_length=128)
    parent = TreeForeignKey('self', on_delete=models.CASCADE)
    timeZ = models.CharField(max_length=128)
    uuid = models.CharField(max_length=64)


class Prices(models.Model):
    '''Подписки'''
    title = models.CharField(max_length=128)
    days = models.PositiveIntegerField(default=90)
    params = models.TextField()


class RoomsTypes(models.Model):
    '''Виды номеров'''
    title = models.CharField(max_length=128)
    params = models.TextField()


class HotelsParams(models.Model):
    '''Параметры отелей'''
    title = models.CharField(max_length=1024)
    params = models.TextField()


class Hotels(models.Model):
    '''Отели'''
    title = models.CharField(max_length=128)
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='place')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    price = models.ForeignKey(Prices, on_delete=models.CASCADE, related_name='price')
    param = models.ManyToManyField('HotelsParams',
                                   through='HotelsParamsHotels',
                                   through_fields=('hotels', 'hotels_params'))
    roomstypes = models.ManyToManyField('RoomsTypes',
                                        through='RoomsTypesHotels',
                                        through_fields=('hotels', 'room_types'))
    www = models.CharField(max_length=1024)
    volume = models.PositiveIntegerField(default=0)
    pms = models.CharField(max_length=128)
    params = models.TextField()


class RoomsTypesHotels(models.Model):
    '''Виды номеров-Отели Клиента'''
    hotels = models.ForeignKey('Hotels', on_delete=models.CASCADE, related_name='hotels_room')
    room_types = models.ForeignKey('RoomsTypes', on_delete=models.CASCADE, related_name='room_types')
    title = models.CharField(max_length=128)
    value = models.PositiveIntegerField(default=0)
    params = models.TextField()


class HotelsParamsHotels(models.Model):
    '''Параметры отелей-Отели Клиента'''
    hotels = models.ForeignKey('Hotels', on_delete=models.CASCADE, related_name='hotels_hotel')
    hotels_params = models.ForeignKey('HotelsParams', on_delete=models.CASCADE, related_name='hotels_params')
    title = models.CharField(max_length=128)
    params = models.TextField()
