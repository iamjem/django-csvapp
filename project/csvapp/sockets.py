from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from csvapp.pubsub import subscribe, unsubscribe


@namespace('/csv')
class CSVNamespace(BaseNamespace):
    def initialize(self):
        pass

    def disconnect(self, *args, **kwargs):
        super(CSVNamespace, self).disconnect(*args, **kwargs)
        unsubscribe(
            'csvapp.user.{}'.format(self.request.user),
            self.subscribe_handler)

    def recv_connect(self):
        if self.request.user.is_authenticated():
            subscribe(
                'csvapp.user.{}'.format(self.request.user),
                self.subscribe_handler)
        else:
            self.disconnect()

    def subscribe_handler(self, data):
        print 'got data'
        print data
