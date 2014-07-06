from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from csvapp.models import Document, SortedDocument
from csvapp.tests.mixins import SignalMixin, LoginMixin
from csvapp.tests.utils import create_file


class DocumentTestCase(SignalMixin, LoginMixin, APITestCase):
    def test_list_noauth(self):
        url = reverse('document-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            'document-list should require auth')

    def test_list_auth(self):
        url = reverse('document-list')
        self.do_login()
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'document-list should return HTTP 200')
        self.assertEqual(
            response.data,
            [],
            'document-list should have no data')

    def test_create_bad_extension(self):
        url = reverse('document-list')
        self.do_login()
        response = self.client.post(url, {
            'file': SimpleUploadedFile('doc.pdf', 'blahblah')
        })

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            'document-list post should require valid file extension')

    def test_create(self):
        url = reverse('document-list')
        self.do_login()
        response = self.client.post(url, {
            'file': SimpleUploadedFile('doc.csv', 'blahblah')
        })

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'document-list post should return HTTP 201')

    def test_detail_noauth(self):
        url = reverse('document-detail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            'document-detail should require auth')

    def test_detail_auth(self):
        url = reverse('document-detail', kwargs={'pk': 1})
        self.do_login()
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            'document-detail should return HTTP 404')

    def test_delete_noauth(self):
        url = reverse('document-detail', kwargs={'pk': 1})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            'document-detail should require auth')

    def test_delete(self):
        self.disconnect_signals()
        self.do_login()

        doc = Document.objects.create(
            user=self.user,
            file=SimpleUploadedFile('doc.csv', 'blahblah'))

        url = reverse('document-detail', kwargs={'pk': doc.id})
        response = self.client.delete(url)

        self.reconnect_signals()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            'document-list delete should return HTTP 204')


class SortedDocumentTestCase(SignalMixin, LoginMixin, APITestCase):
    def test_list_noauth(self):
        url = reverse('sorted-document-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            'sorted-document-list should require auth')

    def test_list_auth(self):
        url = reverse('sorted-document-list')
        self.do_login()
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'document-list should return HTTP 200')
        self.assertEqual(
            response.data,
            [],
            'sorted-document-list should have no data')

    def test_create(self):
        url = reverse('sorted-document-list')
        self.do_login()

        file = create_file()
        doc = Document.objects.create(
            user=self.user,
            file=SimpleUploadedFile('doc.csv', file.read()))
        file.close()

        response = self.client.post(url, {
            'doc': doc.id,
            'column': 'A'
        })

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'sorted-document-list post should return HTTP 201')

    def test_detail_noauth(self):
        url = reverse('sorted-document-detail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            'sorted-document-detail should require auth')

    def test_detail_auth(self):
        url = reverse('sorted-document-detail', kwargs={'pk': 1})
        self.do_login()
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            'sorted-document-detail should return HTTP 404')

    def test_delete_noauth(self):
        url = reverse('sorted-document-detail', kwargs={'pk': 1})
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            'sorted-document-detail should require auth')

    def test_delete(self):
        self.disconnect_signals()
        self.do_login()

        file = create_file()
        doc = Document.objects.create(
            user=self.user,
            file=SimpleUploadedFile('doc.csv', file.read()))
        file.close()

        sorted_doc = SortedDocument.objects.create(
            doc=doc,
            column='A')


        url = reverse('sorted-document-detail', kwargs={'pk': sorted_doc.id})
        response = self.client.delete(url)

        self.reconnect_signals()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            'document-list delete should return HTTP 204')
