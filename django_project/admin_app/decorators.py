from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class SuperuserRequiredMixin(object):
    '''декоратор для проверки прав суперпользователя'''
    @method_decorator(user_passes_test(lambda u: u.is_authenticated and u.is_superuser or u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)
