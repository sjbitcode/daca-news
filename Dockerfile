FROM python:3.8.6-alpine3.12

ENV APP_PATH=/app \
    PYTHONUNBUFFERED=1

WORKDIR $APP_PATH

# Install system dependencies.
RUN apk add --no-cache bash tini openssl


# Copy requirements and install.
COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    --no-warn-script-location \
    -r requirements.txt

COPY . $APP_PATH

EXPOSE 8000

# Run entrypoint with Tini
ENTRYPOINT ["/sbin/tini", "--", "/app/bin/entrypoint.sh"]
