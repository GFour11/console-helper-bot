FROM python:3.10

COPY . /console-bot

WORKDIR /console-bot/

RUN python setup.py install

CMD ["console-bot"]

