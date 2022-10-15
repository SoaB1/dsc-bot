FROM python:3.10.7-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
    jq

RUN pip install --upgrade pip
WORKDIR /root/dsc-bot

COPY requirements.txt /root/dsc-bot
COPY main.py /root/dsc-bot
COPY cog/ /root/dsc-bot/cog
COPY src/ /root/dsc-bot/src
COPY ./entrypoint.sh /entrypoint.sh

RUN pip install -r requirements.txt

ENV TOKEN='TH1515N0TT0KEN' \
    SHEET_URL='https://docs.google.com/spreadsheets/' \
    FORM_URL='https://docs.google.com/forms/'

ENTRYPOINT [ "/entrypoint.sh" ]