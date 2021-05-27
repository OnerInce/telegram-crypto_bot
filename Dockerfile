FROM python:3.8-slim-buster

LABEL maintainer="Oner Ince"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./exchange_bot.py" ]