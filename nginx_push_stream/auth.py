from urllib import parse

from django.http import HttpResponseBadRequest, HttpResponse

from nginx_push_stream import const
from nginx_push_stream.conf import settings


def auth_request(request):
    """This view can be used internally by nginx to decide, if a given request
    is authorised to subscribe to specific queues"""
    original_uri = request.META.get('HTTP_X_ORIGINAL_URI')

    if not original_uri:
        return HttpResponseBadRequest("Please set X-Original-Uri header")

    # original_uri - if set - will look like:
    #
    # '/ws/my-app__all__/my-app__authorized__/my-app__session__28qbe5yfd2n3mc7r52asi9r3yyegsljy?_=1547992190211&tag=&time=&eventid='
    #

    prefix = getattr(settings, "NGINX_PUSH_STREAM_PUB_PREFIX")

    # Use only path of original_uri, don't care about the query string:
    path = parse.urlparse(original_uri).path

    # By default, allow:
    allowed = True

    # Traverse through the whole original_uri, finding elements starting with app prefix.
    # Elements starting with app prefix are channel names. Interesting channel names
    # are defined in nginx_push_stream.const, __all__, __session__, __authorised__ .

    # The channel __uuid__ is for web page uuids and the user is always authorised by
    # the sole fact of knowing the web page UUID, so there are no checks.

    for elem in path.split("/"):
        # If current path element is empty or is not starting with app prefix,
        # just forget it and get the next one:
        if not elem or not elem.startswith(prefix):
            continue

        # If an element starts with the app prefix, it's a channel name:
        channel = elem[len(prefix):]

        # __all__: this channel is allowed for all users
        if channel.startswith(const.QUEUE_ALL_USERS):
            continue

        # __session__: this channel is only allowed if the request session cookie is
        # identical to the channel name:
        elif channel.startswith(const.QUEUE_SESSION):
            sessionid = channel[len(const.QUEUE_SESSION):]
            if sessionid != request.session.get("session_key"):
                allowed = False

        # __authorised__: this channel is only allowed for logged-in users
        elif channel.startswith(const.QUEUE_ALL_LOGGED):
            if not request.user.is_authenticated:
                allowed = False

        # __uid__: this channel is not checked, by the sole fact of knowing UUID
        elif channel.startswith(const.QUEUE_UUID):
            pass

        # __somethingelse__: this channel name was not defined earlier
        else:
            allowed = False

    if allowed:
        return HttpResponse()

    return HttpResponse(status=403)
