#!/usr/bin/env bash

set -ev

python manage.py migrate

python manage.py install_tailwind

# Do not collect static when in dev environment.
if [ "$DEBUG" != "True" ]; then
    python manage.py collectstatic --noinput
fi

# Run django via gunicorn
gunicorn --reload --bind 0.0.0.0:8000 config.wsgi:application > /app/django_logs 2>&1 &

# Run huey periodic tasks to fetch articles
python manage.py run_huey > /app/huey_logs 2>&1 &

wait -n
