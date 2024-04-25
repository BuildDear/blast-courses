#!/bin/sh

# Зупинити виконання скрипту при помилці
set -e

# Можна додати перевірку залежностей тут (наприклад, очікування бази даних)

# Запуск сервера Django за допомогою gunicorn, використовуючи змінні середовища для конфігурації
exec gunicorn blast_courses.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3}
