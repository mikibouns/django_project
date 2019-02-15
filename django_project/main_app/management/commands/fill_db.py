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

        # Category.objects.all().delete()
        # for category in CATEGORY:
        #     new_category = Category(**category)
        #     new_category.save()
        #
        # HotelCard.objects.all().delete()
        # for hotel_card in HC:
        #     new_hc = HotelCard(**hotel_card)
        #     new_hc.save()
        #
        # HotelRoom.objects.all().delete()
        # for hr in HR:
        #     hr_hotel = hr['hr_hotel']
        #     hr_category = hr['hr_category']
        #     hr_category = Category.objects.get(category_name=hr_category)
        #     hr_hotel = HotelCard.objects.get(hc_name=hr_hotel)
        #     hr['hr_hotel'] = hr_hotel
        #     hr['hr_category'] = hr_category
        #     hr['hr_places'] = randint(1, 5)
        #     hr['hr_price'] = randint(10000, 100000)
        #     new_hr = HotelRoom(**hr)
        #     new_hr.save()
        #
        # ReservedDates.objects.all().delete()
        # for i in range(20):
        #     start_date = datetime.date(randint(2019, 2019), randint(1, 2), randint(1, 28))
        #     last_date = start_date + datetime.timedelta(randint(1, 30))
        #     _id = randint(1, 12)
        #     new_rd = ReservedDates(
        #         # person=User.objects.get(username='User0'),
        #         check_in=start_date,
        #         check_out=last_date,
        #         room=HotelRoom.objects.get(id=_id),
        #     )
        #
        #     new_rd.save()

        # Создаем суперпользователя при помощи менеджера модели
        super_user = HLUsers.objects.create_superuser('root', 'test.mail.django@yandex.ru', 'testtest123')