django-nginx-push-stream
------------------------

Django support library for `Nginx Push Stream Module`_.

.. _Nginx Push Stream Module: https://github.com/wandenberg/nginx-push-stream-module .

Quick introduction
==================

1. `Nginx Push Stream Module`_ is a scalable module for Nginx, that provides pub-sub capabilities.

2. You can install patched Nginx versions containing it:

   * on Ubuntu via `unofficial PPA`_
   * on macOS via `Homebrew`_

3. You can run it by installing `Docker`_, cloning `this repo`_ and typing ``docker-compose up``.
   This command will build the Docker image containing Nginx with `Nginx Push Stream Module`_ and
   start it up. By default, port 80 of Docker container is being mapped to port 9080 of your
   local machine (see `docker-compose.yml`_ for details)

   ::

    ╰─➤  docker-compose up
    Creating network "django-nginx-push-stream_default" with the default driver
    Creating django-nginx-push-stream_nginx_http_push_stream_1 ... done
    Attaching to django-nginx-push-stream_nginx_http_push_stream_1
    nginx_http_push_stream_1  | ==> /var/log/nginx/access.log <==
    nginx_http_push_stream_1  |
    nginx_http_push_stream_1  | ==> /var/log/nginx/error.log <==
    nginx_http_push_stream_1  | 2019/01/15 23:26:42 [info] 8#8: Using 32768KiB of shared memory for push stream module on zone: push_stream_module in /etc/nginx/nginx.conf:15


.. _unofficial PPA: https://launchpad.net/~dotz/+archive/ubuntu/nginx-with-push-stream-module
.. _Homebrew: https://github.com/denji/homebrew-nginx
.. _this repo: https://github.com/mpasternak/django-nginx-push-stream/
.. _Docker: https://www.docker.com/get-started
.. _docker-compose.yml: https://github.com/mpasternak/django-nginx-push-stream/blob/master/docker-compose.yml

