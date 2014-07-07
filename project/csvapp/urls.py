from django.conf.urls import patterns, include, url
from csvapp.views import AppView
from csvapp.forms import BootstrapAuthForm


urlpatterns = patterns('',
    url(r'^', include('csvapp.api.urls')),
    url(r'^$',
        view=AppView.as_view(),
        name='csv_index'
    ),
    url(r'^login/$',
        view='django.contrib.auth.views.login',
        kwargs={
            'template_name': 'csvapp/login.html',
            'authentication_form': BootstrapAuthForm
        },
        name='csv_login'
    ),
    url(r'^logout/$',
        view='django.contrib.auth.views.logout_then_login',
        name='csv_logout'
    ),
)
