# Використання офіційного базового образу Python 3.11 на Alpine для меншого розміру зображення
FROM python:3.11-alpine

# Встановлення залежностей для використання Poetry без необхідності користувача root
RUN pip install poetry

# Створення ненульового користувача
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Встановлення та використання директорії робочої директорії
WORKDIR /usr/src/app

# Копіювання файлів залежностей спершу для кращого кешування шарів
COPY pyproject.toml poetry.lock ./

# Встановлення залежностей з використанням Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копіювання всього проекту
COPY . .

# Встановлення виконавчих дозволів для entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Зміна власника всіх файлів на ненульового користувача
RUN chown -R appuser:appgroup /usr/src/app

# Встановлення користувача для запуску програми
USER appuser

# Встановлення entrypoint.sh як точки входу
ENTRYPOINT ["./entrypoint.sh"]

# Відкриття порту 8000
EXPOSE 8000
