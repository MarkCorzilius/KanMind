#!/bin/sh
set -e

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

python manage.py shell <<EOF

import os
from django.contrib.auth import get_user_model

User = get_user_model()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin@gmail.com')

if not User.objects.filter(email=email).exists():
    print(f"Creating superuser '{email}'...")
    User.objects.create_superuser(email=email, password=password)
    print(f"Superuser '{email}' created.")
else:
    print(f"Superuser '{email}' already exists.")

EOF

exec "$@"