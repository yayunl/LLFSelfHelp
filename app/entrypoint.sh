#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py flush --no-input
python3 manage.py migrate

# Migrate auth user
# python3 manage.py migrate auth
# python3 manage.py migrate

# Create superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python3 manage.py shell

exec "$@"