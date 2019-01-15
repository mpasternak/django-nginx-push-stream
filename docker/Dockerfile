FROM ubuntu:16.04

RUN apt-get -qq update && apt-get -qq install -y \
  software-properties-common  

# This fails because UnicodeBug (I have an 'ł' in my first name...)
RUN add-apt-repository -y "ppa:dotz/nginx-with-push-stream-module" || true

RUN apt-get -qq update \ 
  && DEBIAN_FRONTEND=noninteractive apt-get -qq install -y --allow-unauthenticated \
     nginx-full=1.12.0-1+xenial1+pushtream0

COPY default /etc/nginx/sites-available
COPY nginx.conf /etc/nginx/

EXPOSE 80

RUN nginx -t

ENTRYPOINT nginx && tail -f /var/log/nginx/*