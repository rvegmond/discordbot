FROM --platform=$BUILDPLATFORM python:3-alpine3.12 as build

RUN apk update && apk upgrade && apk add gcc musl-dev
RUN mkdir bot
WORKDIR /bot


COPY requirements.txt /bot/
RUN pip install -r requirements.txt


COPY bot.py __init__.py /bot/
COPY modules /bot/modules

ENTRYPOINT python bot.py

