from django.db import models
from auth_app.models import HLUsers
from django.core.validators import MinValueValidator


class Places(models.Model):
    '''Топонимы'''
    title = models.CharField(max_length=128)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    timeZ = models.CharField(max_length=128)
    uuid = models.CharField(max_length=64)


class Prices(models.Model):
    '''Подписки'''
    title = models.CharField(max_length=128)
    days = models.IntegerField(default=90, validators=[MinValueValidator(1)])
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
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    owner = models.ForeignKey(HLUsers, on_delete=models.CASCADE)
    price = models.ForeignKey(Prices, on_delete=models.CASCADE)
    param = models.ManyToManyField('HotelsParams',
                                   through='HotelsParamsHotels',
                                   through_fields=('hotels', 'hotels_params'))
    roomstypes = models.ManyToManyField('RoomsTypes',
                                        through='RoomsTypesHotels',
                                        through_fields=('hotels', 'room_types'))
    www = models.CharField(max_length=1024)
    volume = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    pms = models.CharField(max_length=128)
    params = models.TextField()


class RoomsTypesHotels(models.Model):
    '''Виды номеров-Отели Клиента'''
    hotels = models.ForeignKey('Hotels', on_delete=models.CASCADE)
    room_types = models.ForeignKey('RoomsTypes', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    value = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    params = models.TextField()


class HotelsParamsHotels(models.Model):
    '''Параметры отелей-Отели Клиента'''
    hotels = models.ForeignKey('Hotels', on_delete=models.CASCADE)
    hotels_params = models.ForeignKey('HotelsParams', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    params = models.TextField()