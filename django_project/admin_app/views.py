from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from .forms import CreateForm, EditForm


class UserList(View):
    users = get_user_model().objects.all().order_by('username')
    template_name = 'admin_app/user_list.html'
    context = {'users': users}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

class UserDetail(DetailView):
    model = get_user_model()


class UserCreate(View):
    initial = {'key': 'value'}
    form_class = CreateForm
    template_name = 'admin_app/user_detail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

class UserUpdate(UpdateView):
    model = get_user_model()


class UserDelete(DeleteView):
    model = get_user_model()