FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.0.1

WORKDIR /app

RUN poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

# Копируем только pyproject.toml и README
COPY pyproject.toml README.md ./

# Генерируем lock и устанавливаем
RUN poetry lock --no-interaction \
    && poetry install --no-interaction --no-ansi --no-root --only main

COPY . .

RUN mkdir -p /app/media /app/staticfiles

EXPOSE 8000