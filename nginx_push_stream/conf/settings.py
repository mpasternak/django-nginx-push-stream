from django.conf import settings

NGINX_PUSH_STREAM_HOST = getattr(settings, "NGINX_PUSH_STREAM_HOST", '127.0.0.1')
NGINX_PUSH_STREAM_PORT = getattr(settings, "NGINX_PUSH_STREAM_PORT", 80)
NGINX_PUSH_STREAM_PROTOCOL = getattr(settings, "NGINX_PUSH_STREAM_PROTOCOL", 'http')
NGINX_PUSH_STREAM_PUB_PREFIX = getattr(settings, "NGINX_PUSH_STREAM_PUB_PREFIX", 'my-app')
