#!/bin/sh

# Зупинити виконання скрипту при помилці
set -e

# Запуск сервера Django за допомогою gunicorn, використовуючи змінні середовища для конфігурації
exec gunicorn blast_courses.wsgi:application --bind 0.0.0.0:"${PORT:-8000}" --workers ${GUNICORN_WORKERS:-3}
