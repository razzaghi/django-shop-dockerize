FROM nginx:1.19.0-alpine

COPY nginx.conf /etc/nginx/conf.d/nginx.conf
#ENV APP_HOME=/home/app/web
#RUN mkdir -p /home/app/web && mkdir -p /home/app/web/static && mkdir -p /home/app/web/media
#WORKDIR /home/app/web

RUN rm /etc/nginx/conf.d/default.conf
