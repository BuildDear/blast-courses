#!/bin/sh

# Зупинити виконання скрипту при помилці
set -e

# Запуск сервера Django без використання Gunicorn
exec python manage.py runserver 0.0.0.0:${PORT:-8000}