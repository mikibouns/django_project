from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from subprocess import call
import os
from transliterate import translit

# from main_app.models import Places


slash = r'/'
if os.name == 'nt':
    slash = '\\'

try:
    # os.remove('db.sqlite3')
    os.remove(r'main_app{}migrations{}0001_initial.py'.format(slash))
    os.remove(r'auth_app{}migrations{}0001_initial.py'.format(slash))
except:
    print('Not found!')

    call('python manage.py makemigrations', shell=True)
    call('python manage.py migrate', shell=True)


def users_iterator():
    '''генератор создание пользователей'''
    FIOs = [['Иванов', 'Иван', 'Иванович'],
            ['Петров', 'Петр', 'Петрович'],
            ['Сидоров', 'Сергей', 'Федорович'],
            ['Путин', 'Владимир', 'Владимирович'],
            ['Пушкин', 'Александр', 'Сергеевич'],
            ['Пупкин', 'Владимир', 'Петрович']]
    for i in FIOs:
        user = get_user_model()(
            first_name=i[1],
            lastname=i[0],
            surname=i[2],
            email='{}@mail.com'.format(translit(i[0], reversed=True).lower()),
            username=translit(i[0], reversed=True).lower(),
        )
        user.set_password('123')
        yield user


class Command(BaseCommand):
    def handle(self, *args, **options):
        # заполнение топонимов
        # contry = Places.objects.create(title='Russia', uuid='2017370')
        # with open('Ru.txt', 'r', encoding='utf-8') as f:
        #     for line in f:
        #         info_list = line.split('\t')
        #         Places.objects.create(uuid=info_list[0], timeZ=info_list[-2], title=info_list[1], parent=contry)

        get_user_model().objects.bulk_create(iter(users_iterator())) # создание пользователей

        # Создаем суперпользователя при помощи менеджера модели
        super_user = get_user_model().objects.create_superuser('root', 'test.mail.django@yandex.ru', 'testtest123')

        call('python manage.py sitetree_resync_apps main_app', shell=True)