FROM php:8.1-apache

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y \
    nano \
    sed  \
    curl \
    git \
    iproute2 \
    software-properties-common

RUN apt-get update

RUN apt-get update && apt-get install -y \
    qgis \
    python3-qgis

RUN a2enmod proxy_http
RUN a2enmod headers


RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs
RUN npm install -g forever


COPY .docker/service.conf /etc/apache2/sites-available/service.conf


