from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateForm, EditForm
from django.contrib.auth.decorators import user_passes_test
from django.views import View

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
            'FIO': fio,
        }
        return fio_dict


class UserList(ListView):
    '''список пользователей(администраторов)'''
    model = get_user_model()
    template_name = 'admin_app/user_list.html'


class UserDetail(DetailView):
    '''поисание пользователя и опции'''
    model = get_user_model()
    template_name = 'admin_app/user_detail.html'


class UserCreate(CreateView):
    '''создание нового пользователя'''
    form_class = CreateForm
    template_name = 'admin_app/user_create_update.html'

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_model = get_user_model()
        form = self.form_class(data=request.POST)
        if form.is_valid():
            data_create = {
                'username': request.POST.get('username', ''),
                'email': request.POST.get('email', ''),
                'password': request.POST.get('password', '')
            }
            data_create.update(fio_converter(request.POST.get('FIO', '')))
            new_user = user_model.objects.create_user(**data_create)

            return HttpResponseRedirect(reverse('admin_panel:user_detail', args=(new_user.id, )))
        return HttpResponseRedirect(reverse('admin_panel:user_create'))


class UserUpdate(UpdateView):
    template_name = 'admin_app/user_create_update.html'
    form_class = EditForm

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        form = self.form_class(initial=self.create_initial_dict(user))
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs)):


    def create_initial_dict(self, instance):
        fio = fio_converter(instance)
        instance_dict = {
            'email': instance.email,
            'username': instance.username,
        }
        instance_dict.update(fio)
        return instance_dict


class UserDelete(View):
    '''удаление пользователя'''
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()
        # user.is_active = False
        # user.save()
        return HttpResponseRedirect(reverse('admin_panel:user_list'))
