FROM python:3-alpine3.12

RUN apk update && apk upgrade && apk add gcc musl-dev
RUN mkdir bot
WORKDIR /bot


COPY requirements.txt /bot/
RUN pip install -r requirements.txt


COPY bot.py __init__.py /bot/

ENTRYPOINT python __init__.py

