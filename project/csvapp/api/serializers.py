import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from csvapp.models import Document, SortedDocument


CSV_PATTERN = re.compile(r'^.+\.csv$', re.I)
CSV_CONTENT_TYPES = ('text/csv', 'text/plain')


class DocumentSerializer(serializers.ModelSerializer):
    # TODO: Should set user field manually?
    sorted_documents = serializers.RelatedField(many=True)

    class Meta:
        model = Document
        fields = ('id', 'file', 'column_names', 'created',
                  'sorted_documents')

    def validate_file(self, attrs, source):
        value = attrs[source]

        # Check file extension
        if not CSV_PATTERN.match(value.name):
            raise serializers.ValidationError('Invalid file format.')

        # Check content type
        if value.content_type not in CSV_CONTENT_TYPES:
            raise serializers.ValidationError('Invalid content type.')

        return attrs


class SortedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortedDocument
        fields = ('id', 'doc', 'file', 'column', 'created')

    def validate_doc(self, attrs, source):
        value = attrs[source]
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(
                'You must own the document to be sorted.')
        return attrs

    def validate_column(self, attrs, source):
        value = attrs[source]
        if value not in attrs['doc'].column_names:
            raise serializers.ValidationError(
                'Invalid column name.')
        return attrs
