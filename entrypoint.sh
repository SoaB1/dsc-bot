#!/bin/ash
# shellcheck shell=dash

set -e

logDate() {
    LANG=en_US.UTF-8
    LOGDATE=$(date '+%Y-%m-%d(%a) %H:%M:%S')
    export LOGDATE
}

logInfo() {
    logDate
    echo "[${LOGDATE}][INFO] $1"
}

logWarn() {
    logDate
    echo "[${LOGDATE}][WARN] $1"
}

logErr() {
    logDate
    echo "[${LOGDATE}][ERROR] $1"
}

JSON_FILE=$(find /root/dsc-bot/ -maxdepth 1 -type f -name "*.json")

if [ -f "${JSON_FILE}" ]; then
    JSON_TYPE=$(jq -r '.type' <"${JSON_FILE}")
    if [ "${JSON_TYPE}" != "service_account" ]; then
        logErr "This is not a service account file."
        logWarn "FILE: ${JSON_FILE}"
        exit 2
    else
        logInfo "Service account file found."
        logInfo "FILE: ${JSON_FILE}"
    fi
else
    logErr "No service account file found."
    exit 1
fi

logInfo "Starting DSC Bot..."
python3 /root/dsc-bot/main.py
