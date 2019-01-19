from django.test import TestCase

from nginx_push_stream.core import publish_message


class TestNginxPushStream(TestCase):
    def test_publish_message(self):
        # Integration test, requires running nginx_push_stream docker box
        publish_message("foo", wtf="lol")
