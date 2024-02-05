FROM python:3.10.13-alpine3.19

# Interrompe la build se un comando fallisce
RUN set -e

# Installa dos2unix
RUN apk add --no-cache dos2unix

COPY . /app
WORKDIR /app


# Installa le dipendenze
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:8000 --worker-tmp-dir /dev/shm TomatoAI.wsgi
