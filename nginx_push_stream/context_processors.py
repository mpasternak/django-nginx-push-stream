from nginx_push_stream.conf import settings


def configuration(request):
    return dict(
        NGINX_PUSH_STREAM_PUB_HOST=getattr(settings, "NGINX_PUSH_STREAM_PUB_HOST"),
        NGINX_PUSH_STREAM_PUB_PORT=getattr(settings, "NGINX_PUSH_STREAM_PUB_PORT"),

        NGINX_PUSH_STREAM_SUB_HOST=getattr(settings, "NGINX_PUSH_STREAM_SUB_HOST"),
        NGINX_PUSH_STREAM_SUB_PORT=getattr(settings, "NGINX_PUSH_STREAM_SUB_PORT"),

        NGINX_PUSH_STREAM_PROTOCOL=getattr(settings, "NGINX_PUSH_STREAM_PROTOCOL"),
        NGINX_PUSH_STREAM_PUB_PREFIX=getattr(settings, "NGINX_PUSH_STREAM_PUB_PREFIX"),
    )
