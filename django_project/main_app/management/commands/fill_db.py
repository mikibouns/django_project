from django.core.management.base import BaseCommand
# from main_app.models import Hotels
from django.contrib.auth import get_user_model
from subprocess import call
import os
import geocoder
from pprint import pprint
from django.utils import timezone
import pytz
import tzlocal


# try:
#     # os.remove('db.sqlite3')
#     os.remove(r'main_app\migrations\0001_initial.py')
#     os.remove(r'auth_app\migrations\0001_initial.py')
# except:
#     print('Not found!')

# call('manage.py makemigrations', shell=True)
# call('manage.py migrate', shell=True)


def users_iterator():
    for i in range(6):
        user = get_user_model()(
            first_name='User{}'.format(i),
            email='user{}@mail.com'.format(i),
            username='User{}'.format(i),
        )
        user.set_password('123')
        yield user


class Command(BaseCommand):
    def handle(self, *args, **options):

        # get_user_model().objects.bulk_create(iter(users_iterator()))
        #
        # # Создаем суперпользователя при помощи менеджера модели
        # super_user = get_user_model().objects.create_superuser('root', 'test.mail.django@yandex.ru', 'testtest123')

        g = geocoder.geonames('Kaliningrad', key='geoname_user_2019') # password: testtest123
        g = geocoder.geonames(g.geonames_id, method='details', key='geoname_user_2019')
        print(g.address)
        print(g.country)
        print(g.geonames_id)
        # pprint(g.timeZoneId)