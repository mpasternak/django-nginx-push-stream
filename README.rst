django-nginx-push-stream
------------------------

Django support library for `Nginx Push Stream Module`_.

Quick introduction
==================

1. `Nginx Push Stream Module`_ is a scalable module for Nginx, that provides pub-sub capabilities.

2. You can install Nginx binaries which include it:

   * on Ubuntu via `unofficial PPA`_
   * on macOS via `Homebrew`_

3. For development, you can run it by installing `Docker`_, cloning this repo and typing
   ``docker-compose up``. This command will build the Docker image containing Nginx with `Nginx Push Stream Module`_ and
   start it up. By default, port 80 of Docker container is being mapped to port 9080 of your
   local machine (see `docker-compose.yml`_ for details)

  .. code-block:: shell

    $  docker-compose up
    Creating network "django-nginx-push-stream_default" with the default driver
    Creating django-nginx-push-stream_nginx_http_push_stream_1 ... done
    Attaching to django-nginx-push-stream_nginx_http_push_stream_1
    nginx_http_push_stream_1  | ==> /var/log/nginx/access.log <==
    nginx_http_push_stream_1  |
    nginx_http_push_stream_1  | ==> /var/log/nginx/error.log <==
    nginx_http_push_stream_1  | 2019/01/15 23:26:42 [info] 8#8: Using 32768KiB of shared memory for push stream module on zone: push_stream_module in /etc/nginx/nginx.conf:15


4. This package, django-nginx-push-stream, is an attempt to unleash the power of the Nginx Push
   Stream Module from Django application.

5. There are various ways to achieve the goal of realtime push notifications in web browser. This approach
   is one of many. Its benefits include not having to run a separate webserver just for handling
   websockets and the ability to use the same address/port for realtime connections as for the rest
   of the web page.

6. This module is a very, very thin layer of code and configuration for Django. It was
   created rather because of a need to clarify, document and sort-out things in general,
   not because sending push messages via `Nginx Push Stream Module`_ is hard. It is not.

Design
======

django-nginx-push-stream consists of:

* configuration settings in conf/settings.py,
* calls in the `core.py` module

django-nginx-push-stream describes ways how to subscribe and then
how to send push notifications to Django's:

* anonymous users,
* logged-in sessions

There's a very bare example project provided. You can extend its functionality
to fit it to a specific purpose. A project will be provided, that extends the
basic functionality in order to bring graphics notifications, progress dialogs
and more as a separate module.

Booting your infrastructure
===========================

Run docker server by typing ``docker-compose up -d`` in the root directory. Then:

Example application
===================

.. code-block:: shell

   $ cd test_project
   $ python manage.py runserver

Details
=======

How to send the message to Nginx pubsub queue
---------------------------------------------

.. code-block:: shell

   $ cd test_project
   $ python manage.py publish_message  -q __all__  -d '{"message": ["Foobar"]}'

This will send a short message to a queue called ``__all__`` which should include all
users of the site, logged-in or not.

Listening for messages
----------------------

You can listen for messages sent in the above step. Assuming you are using the
default configuration:

* with a browser:

  .. code-block:: shell

      $ cd test_project
      $ python manage.py runserver

  Now open http://127.0.0.1:8000 in your web browser to see the example app
  in action.

* with ``curl``:

  .. code-block:: shell

      $ curl -s -v --no-buffer 'http://localhost:9080/sub/my-app__all__'

* with `websocket-client`_:

  .. code-block:: shell

      $ pip install websocket-client

  then:

  .. code-block:: python

      from websocket import create_connection
      ws = create_connection("ws://localhost:9080/ws/my-app__all__")
      print("Listening...")
      result = ws.recv()
      print("Received '%s'" % result)
      ws.close()

As you probably already know, the ``__all__`` string portion of URL is the name of
a queue. ``my-app`` is a prefix, that can be configured by changing
``NGINX_PUSH_STREAM_PUB_PREFIX``.

``curl(1)``? Great! So why do I need a Django app for, exactly?
===============================================================

This package makes it easier to send information to specific sessions or all
users of your Django-based website:

* send message to a specific Django session: browser subscribes to a channel with
  name based on session id (as shown in test_project),

* send message to all users (as shown in test_project),

Not yet shown in examples (patches accepted): 

* send message to all logged-in users: make logged in users subscribe to a queue
  for logged in users,

* give an UUID for every single web page that gets rendered by your server and send
  messages only to this page (with help of `django-template-uuid`_)

Security
========

Anyone can subscribe to a queue with the default configuration. So, a malicous attacker
could subscribe and read users private information. How to avoid this? Nginx documentation
has a section about `Authentication based on subrequest result`_ . Currently this is not
shown or documented in example code of this project and it definitely could be. Patches
welcome.

WebSockets vs SSE
=================

`Nginx Push Stream Module`_ offers sending messages over both WebSockets and EventSource (SSE).
You can read about those two different approaches on `StackOverflow`_.

.. _Nginx Push Stream Module: https://github.com/wandenberg/nginx-push-stream-module .
.. _unofficial PPA: https://launchpad.net/~dotz/+archive/ubuntu/nginx-with-push-stream-module
.. _Homebrew: https://github.com/denji/homebrew-nginx
.. _Docker: https://www.docker.com/get-started
.. _docker-compose.yml: https://github.com/mpasternak/django-nginx-push-stream/blob/master/docker-compose.yml
.. _Foundation 6: https://foundation.zurb.com
.. _websocket-client: https://pypi.org/project/websocket-client/
.. _django-template-uuid: https://github.com/mpasternak/django-template-uuid
.. _Authentication based on subrequest result: https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
.. _StackOverflow: https://stackoverflow.com/questions/5195452/websockets-vs-server-sent-events-eventsource#5326159
