from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from .forms import CreateUserForm, UpdateUserForm
from django.views import View
from .decorators import SuperuserRequiredMixin
from pprint import pprint


def fio_converter(data):
    '''ф-ция возвращает словарь.
     если str: разбивает по пробелу и составляет словарь
     если QuerySet: составляет строку из определенных полей'''
    if isinstance(data, str):
        fio = str(data).split(' ')
        fio_dict = {
            'first_name': fio[1],
            'lastname': fio[0],
            'surname': fio[2]
        }
        return fio_dict
    else:
        fio = '{} {} {}'.format(data.lastname,
                                data.first_name,
                                data.surname)
        fio_dict = {
            'fio': fio,
        }
        return fio_dict


class UserList(SuperuserRequiredMixin, ListView):
    '''список пользователей(администраторов)'''
    model = get_user_model()
    template_name = 'admin_app/user_list.html'


class UserDetail(SuperuserRequiredMixin, DetailView):
    '''поисание пользователя и опции'''
    model = get_user_model()
    template_name = 'admin_app/user_detail.html'


class UserCreate(SuperuserRequiredMixin, View):
    '''создание нового пользователя'''
    title = 'создать'
    initial = {'is_active': True}
    form_class = CreateUserForm
    template_name = 'admin_app/user_create_update.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'title': self.title})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            fio = fio_converter(form.data['fio'])
            data = form.clean().pop('fio', '')
            data.pop('confirm_password', '')
            data.update(fio)
            new_user = get_user_model().objects.create_user(**data)

            return HttpResponseRedirect(reverse('admin_panel:user_detail', args=(new_user.id, )))
        return render(request, self.template_name, {'form': form, 'title': self.title})


class UserUpdate(SuperuserRequiredMixin, View):
    title = 'обновить'
    template_name = 'admin_app/user_create_update.html'
    form_class = UpdateUserForm

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        form = self.form_class(initial=self.create_initial_dict(user))
        context = {'form': form,
                   'title': self.title,
                   'object': user}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        form = self.form_class(data=request.POST)
        if form.has_changed() and form.is_valid():
            data = form.clean() # получаем значения полей формы в виде словаря
            del_keys = ['fio', 'password', 'confirm_password'] # поля которые необходимо исключить перед обновлением
            fio = fio_converter(form.data['fio']) # превращаем поле fio в словарь
            data.update(fio) # объеденяем словари
            for key in del_keys: # удаляем лишние поля из словаря по ключу
                data.pop(key, '')
            print(data)
            # new_user = get_user_model().objects.filter(id=pk).update(**data)
            # return HttpResponseRedirect(reverse('admin_panel:user_detail', args=(new_user.id,)))
        return render(request, self.template_name, {'form': form, 'title': self.title, 'object': user})

    def create_initial_dict(self, instance):
        fio = fio_converter(instance)
        instance_dict = {
            'email': instance.email,
            'username': instance.username,
            'is_active': instance.is_active,
            'is_staff': instance.is_staff
        }
        instance_dict.update(fio)
        return instance_dict


class UserDelete(SuperuserRequiredMixin, View):
    template_name = 'admin_app/delete_confirmation.html'

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        context = {'object': user}
        return render(request, self.template_name, context)

    def post(self, pk, *args, **kwargs):
        '''удаление пользователя'''
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()
        # user.is_active = False
        # user.save()
        return HttpResponseRedirect(reverse('admin_panel:user_list'))
