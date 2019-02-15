from django.core.management.base import BaseCommand
from main_app.models import Hotels
from auth_app.models import HLUsers
from subprocess import call
import os


try:
    os.remove('db.sqlite3')
    os.remove(r'main_app\migrations\0001_initial.py')
    os.remove(r'auth_app\migrations\0001_initial.py')
except:
    print('Not found!')

call('manage.py makemigrations', shell=True)
call('manage.py migrate', shell=True)


def users_iterator():
    for i in range(6):
        user = HLUsers(
            first_name='User{}'.format(i),
            email='user{}@mail.com'.format(i),
            username='User{}'.format(i),
        )
        user.set_password('123')
        yield user


class Command(BaseCommand):
    def handle(self, *args, **options):

        HLUsers.objects.bulk_create(iter(users_iterator()))

        # Создаем суперпользователя при помощи менеджера модели
        super_user = HLUsers.objects.create_superuser('root', 'test.mail.django@yandex.ru', 'testtest123')