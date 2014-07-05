try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import pandas as pd
from threading import Event
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db.models.signals import post_save
from django.test import TestCase
from csvapp.tasks import clean_and_update_document
from csvapp.models import Document
from csvapp.pubsub import broadcaster, subscribe
from csvapp.signals import post_save_document


class DocumentTaskTestCase(TestCase):
    def tearDown(self):
        broadcaster._reset_handlers()

    def disconnect_signals(self):
        post_save.disconnect(post_save_document, sender=Document)

    def reconnect_signals(self):
        post_save.connect(post_save_document, sender=Document)

    def create_document_with_duplicates(self):
        df = pd.DataFrame({
            'A': ['Foo', 'Bar', 'Foo', 'Bar', 'Foo'],
            'B': ['Bar', 'Bar', 'Foo', 'Foo', 'Foo']
        })
        out = StringIO()
        df.to_csv(out, index=False)
        out.seek(0)
        out.flush()

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
