from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from .forms import CreateUserForm, UpdateUserForm
from django.views import View
from .decorators import SuperuserRequiredMixin
from pprint import pprint
from django.db.models import Q


class UserList(SuperuserRequiredMixin, ListView):
    '''список пользователей(администраторов)'''
    model = get_user_model()
    template_name = 'admin_app/user_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.exclude(Q(is_superuser=True) | Q(is_staff=True))


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
            fio = form.cleaned_data.pop('fio', '') # удаляем ключ fio и получаем его значение
            new_user = form.save()
            get_user_model().objects.filter(id=new_user.id).update(**fio)
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
            form.delete_fields() # удалить поля is_active и is_staff
        context = {'form': form,
                   'title': self.title,
                   'object': user}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        form = self.form_class(request.POST, request.FILES)
        if user.is_superuser: # если выбранный пользователь superuser
            form.delete_fields() # удалить поля is_active и is_staff
        if form.has_changed() and form.is_valid():
            fio = form.cleaned_data.pop('fio', '') # удаляем ключ fio и получаем его значение
            data = {**form.cleaned_data, **fio}
            changed_data = data.copy() # создаем копию словаря которую будем изменять
            for key, val in data.items(): # обходим словарь в цикле
                if val == '' or key == 'confirm_password' or key == 'password':
                    changed_data.pop(key, None) # в созданной копии словаря вносим изменения
            get_user_model().objects.filter(pk=pk).update(**changed_data)
            if data['password']: # если пароль указан
                user.set_password(data['password']) # тогда обновить пароль
                user.save() # сохраняем внесенные изменения
            return HttpResponseRedirect(reverse('admin_panel:user_detail', args=(user.id,)))
        return render(request, self.template_name, {'form': form, 'title': self.title, 'object': user})

    def create_initial_dict(self, instance):
        '''создает словарь для инициализации полей формы при обновлении'''
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
