# -*- encoding: utf-8 -*-
import json
from urllib import request
from urllib.parse import urlunparse, urlencode

from nginx_push_stream.conf import settings


def get_pub_path(s):
    """Adds Django application prefix to pub path"""
    prefix = getattr(settings, "NGINX_PUSH_STREAM_PUB_PREFIX", "PUB_PREFIX_unset")
    return {"id": prefix + s}


def build_url(pub_path):
    proto = getattr(settings, "NGINX_PUSH_STREAM_PROTOCOL")
    host = getattr(settings, "NGINX_PUSH_STREAM_HOST")
    port = getattr(settings, "NGINX_PUSH_STREAM_PORT")
    url = urlunparse(
        (proto, f"{host}:{port}", "pub/", "", urlencode(get_pub_path(pub_path)), "")
    )
    return url


def publish_message(pub_path, **message):
    url = build_url(pub_path)
    message_json = json.dumps(message).encode('utf-8')
    req = request.Request(url, data=message_json)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(message_json))
    response = request.urlopen(req)

    # When you have the return value - the response - you can:
    #
    # >>> res = response.read()
    # >>> json.loads(res)
    # {'channel': 'my-app-foo', 'published_messages': 1, 'stored_messages': 0, 'subscribers': 0}
    #

    return response
