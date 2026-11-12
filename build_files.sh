#!/usr/bin/env bash
# Build step only: collect static files. Run migrations as a SEPARATE release step:
#   python manage.py migrate --noinput
set -euo pipefail
python manage.py collectstatic --noinput
