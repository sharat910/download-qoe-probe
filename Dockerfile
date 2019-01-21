FROM python:3.6-alpine3.8

RUN apk add --no-cache tzdata wget

ENV TZ Australia/Sydney

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip

RUN pip install -U selenium requests pyyaml pytz

RUN mkdir /app

WORKDIR /app

COPY . /app