from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class AppView(TemplateView):
    template_name = 'csvapp/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AppView, self).dispatch(*args, **kwargs)
