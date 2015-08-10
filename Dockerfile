FROM python:2-onbuild
MAINTAINER Ivan Kurakin <ivancurachin@gmail.com>
RUN mkdir -p /srv/services/pop3_server
WORKDIR /srv/services/pop3_server
COPY . /srv/services/pop3_server
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "/srv/services/pop3_server/server.py" ]
EXPOSE 1110
