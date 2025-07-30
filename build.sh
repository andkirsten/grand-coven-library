#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Clear any existing staticfiles
rm -rf staticfiles/

# Collect static files
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate 