#!/bin/bash
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

authAccount() {
    local account_name="$1"
    local account_key="$2"

    if [ "$(gcloud auth list --filter=status:ACTIVE --format="value(account)")" != "${account_name}" ]; then
        logInfo "Authenticating Service Account..."
        gcloud auth activate-service-account "${account_name}" --key-file="${account_key}"
        if [ "$(gcloud auth list --filter=status:ACTIVE --format="value(account)")" = "${account_name}" ]; then
            logInfo "Service Account authenticated."
        else
            logErr "Service Account authentication failed."
            exit 1
        fi
    else
        logInfo "Service Account already authenticated."
    fi
}

JSON_PATH=$(find /cloud-bot/ -maxdepth 1 -type f -name "*.json")

if [ -f "${JSON_PATH}" ]; then
    JSON_TYPE=$(jq -r '.type' <"${JSON_PATH}")
    if [ "${JSON_TYPE}" != "service_account" ]; then
        logErr "This is not a service account file."
        logWarn "FILE: ${JSON_PATH}"
        exit 2
    else
        logInfo "Service account file found."
        logInfo "FILE: ${JSON_PATH}"
        GOOGLE_APPLICATION_CREDENTIALS="${JSON_PATH}"
        SERVICE_ACCOUNT_NAME=$(jq -r '.client_email' <"${JSON_PATH}")
        PROJECT_ID=$(jq -r '.project_id' <"${JSON_PATH}")
        export GOOGLE_APPLICATION_CREDENTIALS
        export SERVICE_ACCOUNT_NAME
        export PROJECT_ID
        authAccount "${SERVICE_ACCOUNT_NAME}" "${GOOGLE_APPLICATION_CREDENTIALS}"
    fi
    logInfo "Starting build-cloud-bot..."
    python3 /cloud-bot/main.py
else
    logErr "No service account file found."
    exit 1
fi
