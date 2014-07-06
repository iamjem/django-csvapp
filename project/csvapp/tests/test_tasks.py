import pandas as pd
from pandas.util.testing import assert_series_equal
from threading import Event
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from csvapp.tasks import clean_and_update_document, create_sorted_document_file
from csvapp.models import Document, SortedDocument
from csvapp.pubsub import broadcaster, subscribe
from csvapp.tests.mixins import SignalMixin
from csvapp.tests.utils import create_file


class DocumentTaskTestCase(SignalMixin, TestCase):
    def tearDown(self):
        broadcaster._reset_handlers()

    def create_document_with_duplicates(self):
        out = create_file()
        self.user = get_user_model().objects.create_user(
            username='foo', password='bar')
        self.doc = Document.objects.create(
            user=self.user, file=File(out, name='doc.csv'))
        out.close()

    def test_document_with_duplicates(self):
        self.disconnect_signals()
        self.create_document_with_duplicates()

        result = clean_and_update_document.delay(self.doc.id)
        meta = result.get()

        self.reconnect_signals()

        self.assertEqual(meta,
        {
            'event_name': 'document',
            'data': {
                'id': self.doc.id,
                'duplicates': 1,
                'columns': {
                    'A': {'duplicates': 3},
                    'B': {'duplicates': 3}
                }
            }
        }, 'csv with duplicates should produce correct meta')

    def test_document_publishes(self):
        self.disconnect_signals()
        self.create_document_with_duplicates()
        pub_event = Event()

        def handler(data):
            pub_event.set()

        subscribe('csvapp.user.{}'.format(self.user.id), handler)

        result = clean_and_update_document.delay(self.doc.id)
        meta = result.get()

        self.reconnect_signals()
        pub_event.wait(0.5)

        self.assertTrue(
            pub_event.is_set(),
            'document task should publish data')


class SortedDocumentTaskTestCase(SignalMixin, TestCase):
    def tearDown(self):
        broadcaster._reset_handlers()

    def create_document(self):
        out = create_file({
            'A': ['A', 'B', 'C'],
            'B': ['Bar', 'Bar', 'Foo']
        })
        self.user = get_user_model().objects.create_user(
            username='foo', password='bar')
        self.doc = Document.objects.create(
            user=self.user, file=File(out, name='doc.csv'))
        out.close()

    def test_sorted_asc(self):
        self.disconnect_signals()
        self.create_document()

        self.sorted_doc = SortedDocument.objects.create(
            doc=self.doc, column='A', ascending=True)

        result = create_sorted_document_file.delay(self.sorted_doc.id)
        meta = result.get()

        self.reconnect_signals()
        self.sorted_doc = SortedDocument.objects.get(pk=self.sorted_doc.id)

        # Load contents into pandas
        self.sorted_doc.file.open(mode='rb')
        txt_iter = pd.read_csv(
            self.sorted_doc.file,
            iterator=True,
            chunksize=1024 * 64)
        df = pd.concat(txt_iter, ignore_index=True)
        self.sorted_doc.file.close()

        expected = pd.Series(['A', 'B', 'C'])

        try:
            assert_series_equal(expected, df['A'])
            is_equal = True
        except AssertionError:
            is_equal = False

        self.assertTrue(is_equal, 'ascending sort should match expected')

    def test_sorted_desc(self):
        self.disconnect_signals()
        self.create_document()

        self.sorted_doc = SortedDocument.objects.create(
            doc=self.doc, column='A', ascending=False)

        result = create_sorted_document_file.delay(self.sorted_doc.id)
        meta = result.get()

        self.reconnect_signals()
        self.sorted_doc = SortedDocument.objects.get(pk=self.sorted_doc.id)

        # Load contents into pandas
        self.sorted_doc.file.open(mode='rb')
        txt_iter = pd.read_csv(
            self.sorted_doc.file,
            iterator=True,
            chunksize=1024 * 64)
        df = pd.concat(txt_iter, ignore_index=True)
        self.sorted_doc.file.close()

        expected = pd.Series(['C', 'B', 'A'])

        try:
            assert_series_equal(expected, df['A'])
            is_equal = True
        except AssertionError:
            is_equal = False

        self.assertTrue(is_equal, 'descending sort should match expected')
