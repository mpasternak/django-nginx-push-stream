from nginx_push_stream.conf import settings


def configuration(request):
    return dict(
        NGINX_PUSH_STREAM_HOST=getattr(settings, "NGINX_PUSH_STREAM_HOST"),
        NGINX_PUSH_STREAM_PORT=getattr(settings, "NGINX_PUSH_STREAM_PORT"),
        NGINX_PUSH_STREAM_PROTOCOL=getattr(settings, "NGINX_PUSH_STREAM_PROTOCOL"),
        NGINX_PUSH_STREAM_PUB_PREFIX=getattr(settings, "NGINX_PUSH_STREAM_PUB_PREFIX"),
    )
