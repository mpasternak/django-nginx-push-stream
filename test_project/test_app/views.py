from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView

from nginx_push_stream.const import QUEUE_ALL_USERS
from nginx_push_stream.core import publish_message


class TestAppView(TemplateView):
    template_name = "test_app.html"


def message_received(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    r = publish_message(QUEUE_ALL_USERS, **request.POST)

    return HttpResponse(r.read())
