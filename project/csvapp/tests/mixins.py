from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from csvapp.models import Document, SortedDocument
from csvapp.signals import post_save_document, post_save_sorted_document


class SignalMixin(object):
    def disconnect_signals(self):
        post_save.disconnect(post_save_document, sender=Document)
        post_save.disconnect(post_save_sorted_document, sender=SortedDocument)

    def reconnect_signals(self):
        post_save.connect(post_save_document, sender=Document)
        post_save.connect(post_save_sorted_document, sender=SortedDocument)


class LoginMixin(object):
    def do_login(self):
        self.user = get_user_model().objects.create_user(
            username='foo', password='bar')
        self.client.login(username='foo', password='bar')
