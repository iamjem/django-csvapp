import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from csvapp.models import Document, SortedDocument
from csvapp.api.fields import JSONField


CSV_PATTERN = re.compile(r'^.+\.csv$', re.I)


class SortedDocumentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        format='%b %d, %Y %I:%M %p %Z',
        read_only=True)

    class Meta:
        model = SortedDocument
        fields = ('id', 'doc', 'file', 'column', 'ascending', 'created')

    def validate(self, attrs):
        doc = attrs['doc']

        if attrs['column'] not in doc.column_names:
            raise serializers.ValidationError(
                'Invalid column name.')

        if doc.user != self.context['request'].user:
            raise serializers.ValidationError(
                'You must own the document to be sorted.')
        return attrs

class DocumentSerializer(serializers.ModelSerializer):
    column_names = JSONField()
    sorted_documents = SortedDocumentSerializer(many=True, read_only=True)
    created = serializers.DateTimeField(
        format='%b %d, %Y %I:%M %p %Z',
        read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'file', 'column_names', 'created',
                  'sorted_documents')

    def validate_file(self, attrs, source):
        value = attrs[source]

        # Check file extension
        if not CSV_PATTERN.match(value.name):
            raise serializers.ValidationError('Invalid file format.')

        return attrs
