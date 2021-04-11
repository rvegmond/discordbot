FROM python:3-alpine3.13

RUN apk update && apk upgrade && apk add gcc musl-dev
RUN mkdir bot
COPY bot.py __init__.py requirements.txt /bot/
COPY modules /bot/modules

WORKDIR /bot

RUN pip install -r requirements.txt

ENTRYPOINT python __init__.py

