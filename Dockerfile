FROM python:3.10.8-bullseye

FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:slim

WORKDIR /cloud-bot
COPY main.py /cloud-bot/main.py
COPY src /cloud-bot/src
COPY cog /cloud-bot/cog
COPY requirements.txt /cloud-bot/requirements.txt
COPY entrypoint.sh /entrypoint.sh

RUN pip install -r requirements.txt
RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

ENV TOKEN='TH1515N0TT0KEN' \
    SHEET_URL='https://docs.google.com/spreadsheets/' \
    FORM_URL='https://docs.google.com/forms/'

ENTRYPOINT ["/entrypoint.sh"]