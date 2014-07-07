import inspect
try:
    import simplejson as json
except ImportError:
    import json
import time
from django.conf import settings
from collections import defaultdict
from gevent import Greenlet, queue
from csvapp.connection import r


class Broadcaster(Greenlet):
    def __init__(self, ):
        super(Broadcaster, self).__init__()
        self._handlers = defaultdict(list)
        self._publish_queue = queue.Queue()
        self._pubsub = None

    def subscribe(self, channel, handler):
        assert callable(handler), 'Subscriber handlers must be callable.'
        try:
            argspec = inspect.getargspec(handler)
        except TypeError:
            try:
                argspec = inspect.getargspec(receiver.__call__)
            except (TypeError, AttributeError):
                argspec = None
        if argspec:
            assert len(argspec[0]) == 1 or (len(argspec[0]) == 2 and
            argspec[0][0] == 'self'), 'Subscriber handlers must accept one ' \
                'positional argument (data).'

        self._handlers[channel].append(handler)

    def unsubscribe(self, channel, handler):
        try:
            self._handlers[channel].remove(handler)
        except ValueError:
            pass

    def publish(self, channel, msg):
        try:
            msg = json.dumps(msg)
        except:
            msg = None
        if msg:
            self._publish_queue.put((channel, msg))

    def _publish(self, msg):
        for handler in self._handlers[msg['channel']]:
            try:
                handler(json.loads(msg['data']))
            except:
                pass

    def _reset_handlers(self):
        self._handlers = defaultdict(list)

    def _run(self):
        self._pubsub = r.pubsub(ignore_subscribe_messages=True)
        self._pubsub.psubscribe('csvapp.*')

        while True:
            # drain publish queue
            try:
                while True:
                    channel, msg = self._publish_queue.get(block=False)
                    r.publish(channel, msg)
            except queue.Empty:
                pass

            # drain subscribe messages
            while True:
                msg = self._pubsub.get_message()
                if msg:
                    self._publish(msg)
                else:
                    break

            time.sleep(0.01)


broadcaster = Broadcaster()
broadcaster.start()

# convenience hooks
publish = broadcaster.publish
subscribe = broadcaster.subscribe
unsubscribe = broadcaster.unsubscribe
