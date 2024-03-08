FROM python:3.11-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update build-base

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.11-alpine

COPY --from=builder /app/wheels /wheels
# COPY g4f /usr/local/lib/python3.11/site-packages/
RUN pip install --no-cache --no-deps /wheels/*

COPY . bot
WORKDIR /bot

CMD python main.py
