web: gunicorn mydjango.wsgi:application --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py createadmin

