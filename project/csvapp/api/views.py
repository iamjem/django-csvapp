from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response
from csvapp import models
from csvapp.api import serializers


class DocumentViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    model = models.Document
    serializer_class = serializers.DocumentSerializer
    permission_classes = (
        permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user


class SortedDocumentViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    model = models.SortedDocument
    serializer_class = serializers.SortedDocumentSerializer
    permission_classes = (
        permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.filter(
            doc__user=self.request.user)
