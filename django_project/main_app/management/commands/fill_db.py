from django.core.management.base import BaseCommand
from main_app.models import Places
from django.contrib.auth import get_user_model
from subprocess import call
import os
import geocoder
from pprint import pprint
from django.utils import timezone


# try:
#     # os.remove('db.sqlite3')
#     os.remove(r'main_app\migrations\0001_initial.py')
#     os.remove(r'auth_app\migrations\0001_initial.py')
# except:
#     print('Not found!')
#
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

        contry = Places.objects.create(title='Russia', uuid='2017370')
        with open('Ru.txt', 'r', encoding='utf-8') as f:
            for line in f:
                info_list = line.split('\t')
                Places.objects.create(uuid=info_list[0], timeZ=info_list[-2], title=info_list[1], parent=contry)

        # get_user_model().objects.bulk_create(iter(users_iterator()))
        #
        # # Создаем суперпользователя при помощи менеджера модели
        # super_user = get_user_model().objects.create_superuser('root', 'test.mail.django@yandex.ru', 'testtest123')

        # russia = geocoder.geonames('Russian', key='geoname_user_2019') # password: testtest123
        # country = geocoder.geonames(russia.geonames_id, method='children', key='geoname_user_2019')
        # regions = geocoder.geonames(country.geonames_id, method='children', key='geoname_user_2019')
        # for region in regions:
        #     for city in geocoder.geonames(region.geonames_id, method='children', key='geoname_user_2019'):
        #         pprint(city)
        # g = geocoder.geonames(g.geonames_id, method='details', key='geoname_user_2019')
        # pprint(g.timeZoneName)
        # g = g.geojson['features'][0]['properties']['geonames_id']

        # gl = geocoder.geonames(451915, method='details', key='geoname_user_2019')
        # pprint(gl.address)
        # pprint()
        # kal = geocoder.geonames('Верея', key='geoname_user_2019', featureClass='A')
        # pprint(kal.address)

        with open('Ru.txt', 'r', encoding='utf-8') as f:
            for line in f:
                info_list = line.split('\t')
                print(info_list[0], info_list[-2], info_list[1])