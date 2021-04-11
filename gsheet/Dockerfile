FROM python:3-alpine3.12

ADD requirements.txt /
ADD entrypoint.py /


RUN pip install -r requirements.txt

ENTRYPOINT /entrypoint.py

