from threading import Event
from django.test import TestCase, SimpleTestCase
from csvapp.pubsub import broadcaster, publish, subscribe


class PubSubTestCase(SimpleTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        broadcaster._reset_handlers()
        print 'tear down!!!'

    def test_subscribe_noncallable(self):
        has_error = False
        try:
            subscribe('csvapp.test', 'this is not callable')
        except AssertionError:
            has_error = True

        self.assertTrue(has_error,
                        'subscribe should raise AssertionError '
                        'when given non-callable handlers')

    def test_subscribe_callable(self):
        has_error = False

        def handler():
            pass

        try:
            subscribe('csvapp.test', handler)
        except AssertionError:
            has_error = True

        self.assertTrue(has_error,
                        'subscribe should require callable with args')

    def test_subscribe_callable_args(self):
        has_error = False

        def handler(data):
            pass

        try:
            subscribe('csvapp.test', handler)
        except AssertionError as e:
            has_error = True

        self.assertFalse(has_error,
            'subscribe should accept callable with one arg')

    def test_publish(self):
        pub_event = Event()

        def handler(data):
            pub_event.set()

        subscribe('csvapp.test', handler)
        publish('csvapp.test', {'foo': True})

        pub_event.wait(0.5)
        self.assertTrue(pub_event.is_set(),
                        'handler should be called when publish')

    def test_publish_data(self):
        pub_event = Event()

        data = {'foo': True}
        data_received = [0]

        def handler(data):
            data_received[0] = data
            pub_event.set()

        subscribe('csvapp.test', handler)
        publish('csvapp.test', data)

        pub_event.wait(0.5)
        self.assertEqual(data, data_received[0],
                        'handler should receive correct data')
