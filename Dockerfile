FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache-dir
RUN pip install gunicorn

COPY . .

# Создаем права на директорию для статических файлов
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --timeout 120 --bind 0.0.0.0:8000"]
