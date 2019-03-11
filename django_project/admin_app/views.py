from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateUserForm, UpdateUserForm
from django.views import View
from .decorators import SuperuserRequiredMixin
from django import forms
from pprint import pprint


def fio_converter(data):
    '''ф-ция возвращает словарь.
    QuerySet: составляет строку из определенных полей'''

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
            data = form.cleaned_data # получаем данные в виде словаря
            fio = data.pop('fio', '') # удаляем ключ fio и получаем его значение
            data.pop('confirm_password', '') # удаляем ключ confirm_password
            data.update(fio)  # полученный словарь из fio добавляем к словарю data
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
        if user.is_superuser: # если выбранный пользователь superuser
            form.fields['is_active'].widget = forms.HiddenInput() # убрать поле is_active
            form.fields['is_active'].label = ''
            form.fields['is_staff'].widget = forms.HiddenInput() # убрать поле is_staff
            form.fields['is_staff'].label = ''
        context = {'form': form,
                   'title': self.title,
                   'object': user}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        form = self.form_class(data=request.POST)
        if form.has_changed() and form.is_valid():
            exclusion_fields = ('fio', 'password', 'confirm_password')
            data = form.cleaned_data # получаем данные в виде словаря
            fio = data.pop('fio', '')  # удаляем ключ fio и получаем его значение
            passwd = data.pop('password', '') # удаляем ключ password и получаем его значение
            list(map(data.__delitem__, filter(data.__contains__, exclusion_fields))) # удаляем ключи согласно списку
            data.update(fio)  # полученный словарь из fio добавляем к словарю data
            get_user_model().objects.filter(pk=pk).update(**data)
            if passwd:
                user.set_password(passwd)
            return HttpResponseRedirect(reverse('admin_panel:user_detail', args=(user.id,)))
        return render(request, self.template_name, {'form': form, 'title': self.title, 'object': user})

    def create_initial_dict(self, instance):
        instance_dict = {
            'fio': '{} {} {}'.format(instance.lastname,
                                     instance.first_name,
                                     instance.surname),
            'email': instance.email,
            'username': instance.username,
            'is_active': instance.is_active,
            'is_staff': instance.is_staff
        }
        return instance_dict


class UserDelete(SuperuserRequiredMixin, View):
    template_name = 'admin_app/delete_confirmation.html'

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        context = {'object': user}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        '''удаление пользователя'''
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()
        # user.is_active = False
        # user.save()
        return HttpResponseRedirect(reverse('admin_panel:user_list'))
