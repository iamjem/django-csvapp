from django.conf import settings
from django.conf.urls import patterns, include, url
from socketio import sdjango
sdjango.autodiscover()


urlpatterns = patterns('',
    url(r'^', include('csvapp.urls')),
    url(r'^socket\.io', include(sdjango.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
