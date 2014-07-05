from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from csvapp.api import views


router = DefaultRouter()
router.register(
    r'documents',
    views.DocumentViewSet,
    base_name='document')
router.register(
    r'sorted_documents',
    views.SortedDocumentViewSet,
    base_name='sorted-document')


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)
