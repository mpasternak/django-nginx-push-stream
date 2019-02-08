# -*- encoding: utf-8 -*
import json

from django.core.management import BaseCommand

from nginx_push_stream.core import publish_message


class Command(BaseCommand):
    help = 'Sends a message to the specified queue'
    args = '<username> <message>'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--queue', required=True,
                            help="queue name, use __all__ for all users")
        parser.add_argument('-d', '--data', required=True,
                            type=json.loads, help="message to send, encoded as JSON")

    def handle(self, *args, **options):
        publish_message(options['queue'], **options['data'])
