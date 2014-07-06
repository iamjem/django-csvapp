from django.conf.urls import patterns, include, url
from csvapp.views import AppView


urlpatterns = patterns('',
    url(r'^', include('csvapp.api.urls')),
    url(r'^csv/$',
        view=AppView.as_view(),
        name='csv_index'
    ),
    url(r'^csv/login/$',
        view='django.contribut.auth.views.login',
        kwargs={
            'template_name': 'csvapp/login.html'
        },
        name='csv_login'
    ),
    url(r'^csv/logout/$',
        view='django.contribut.auth.views.logout_then_login',
        name='csv_logout'
    ),
)
