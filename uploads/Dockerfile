FROM alpine
COPY echo_server.sh /echo_server.sh

RUN apk add --no-cache netcat-openbsd

CMD /echo_server.sh
