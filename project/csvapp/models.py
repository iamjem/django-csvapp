from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from picklefield.fields import PickledObjectField


class Document(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        null=True)
    file = models.FileField(
        upload_to=lambda inst, fn: '{0}/{1}.csv'.format(
            inst.user.id, str(uuid4())),
        verbose_name=_('File'))
    column_names = PickledObjectField(
        verbose_name=_('Column Names'),
        blank=True,
        editable=False
    )
    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class SortedDocument(models.Model):
    doc = models.ForeignKey(
        Document,
        verbose_name=_('Document'),
        related_name='sorted_documents',
        null=True
    )
    file = models.FileField(
        upload_to=lambda inst, fn: '{0}/{1}.csv'.format(
            inst.doc.user.id, str(uuid4())),
        verbose_name=_('File'),
        editable=False,
        blank=True)
    column = models.CharField(
        verbose_name=_('Column'),
        max_length=128
    )
    ascending = models.BooleanField(
        verbose_name=_('Ascending'),
        default=True
    )
    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ['-created']
        unique_together = (
            ('doc', 'column'),
        )
        verbose_name = 'Sorted Document'
        verbose_name_plural = 'Sorted Documents'
