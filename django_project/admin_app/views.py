from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateForm, EditForm
from django.contrib.auth.decorators import user_passes_test
from django.views import View

from pprint import pprint


class UserList(ListView):
    users = get_user_model().objects.all().order_by('username')
    template_name = 'admin_app/user_list.html'
    context = {'users': users}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class UserDetail(DetailView):
    template_name = 'admin_app/user_detail.html'

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        context = {'user': user}
        return render(request, self.template_name, context)


class UserCreate(CreateView):
    initial = {'key': 'value'}
    form_class = CreateForm
    template_name = 'admin_app/user_create_update.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            get_user_model().objects.create()


class UserUpdate(View):
    template_name = 'admin_app/user_create_update.html'
    form_class = EditForm

    def get(self, request, pk, *args, **kwargs):
        user_model = get_user_model()
        user = get_object_or_404(user_model, pk=pk)
        pprint(user)
        form = self.form_class(initial=user['form'])
        context = {'form': form}
        return render(request, self.template_name, context)


class UserDelete(DeleteView):

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()
        # user.is_active = False
        # user.save()
        return HttpResponseRedirect(reverse('admin_panel:user_list'))
