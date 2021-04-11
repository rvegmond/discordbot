FROM python:3-alpine3.13

ADD requirements.txt /
ADD gsheet.py /


RUN pip install -r requirements.txt

ENTRYPOINT /gsheet.py

