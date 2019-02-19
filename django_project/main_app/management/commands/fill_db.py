from django.core.management.base import BaseCommand
from main_app.models import Places
from django.contrib.auth import get_user_model
from subprocess import call
import os


try:
    # os.remove('db.sqlite3')
    os.remove(r'main_app\migrations\0001_initial.py')
    os.remove(r'auth_app\migrations\0001_initial.py')
except:
    print('Not found!')

call('manage.py makemigrations', shell=True)
call('manage.py migrate', shell=True)


def users_iterator():
    '''генератор создание пользователей'''
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
        # заполнение топонимов
        contry = Places.objects.create(title='Russia', uuid='2017370')
        with open('Ru.txt', 'r', encoding='utf-8') as f:
            for line in f:
                info_list = line.split('\t')
                Places.objects.create(uuid=info_list[0], timeZ=info_list[-2], title=info_list[1], parent=contry)

        get_user_model().objects.bulk_create(iter(users_iterator())) # создание пользователей

        # Создаем суперпользователя при помощи менеджера модели
        super_user = get_user_model().objects.create_superuser('root', 'test.mail.django@yandex.ru', 'testtest123')