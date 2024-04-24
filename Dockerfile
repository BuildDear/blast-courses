# Використання офіційного базового образу Python 3.11
FROM python:3.11-slim

# Встановлення залежностей для використання Poetry
RUN pip install poetry

# Встановлення та використання директорії робочої директорії
WORKDIR /usr/src/app

# Копіювання та встановлення файлу залежностей
COPY pyproject.toml poetry.lock ./

# Встановлення залежностей з використанням Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копіювання всього проекту
COPY . .

# Встановлення entrypoint.sh як точки входу
ENTRYPOINT ["./entrypoint.sh"]

# Відкриття порту 8000
EXPOSE 8000
