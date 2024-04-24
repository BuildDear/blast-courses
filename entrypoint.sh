#!/bin/sh

# Зупинити виконання скрипту при помилці
set -e

# Запуск сервера Django за допомогою gunicorn
exec gunicorn blast_courses.wsgi:application --bind 0.0.0.0:8000
