from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class DocumentTestCase(APITestCase):
    def do_login(self):
        self.user = get_user_model().objects.create_user(
            username='foo', password='bar')
        self.client.login(username='foo', password='bar')

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
            'document-detail should return HTTP 200')
