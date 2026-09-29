# DrfProject

LMS с курсами, уроками и платежами через Stripe.

## Стек

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL 16
- Redis 7
- Celery + Celery Beat
- JWT (SimpleJWT)
- Stripe API
- Docker + Docker Compose

## Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/ваш_username/DrfProject.git
cd DrfProject
```

### 2. Настройка .env
```bash
cp .env.sample .env
```

## Заполните:

SECRET_KEY — секретный ключ

STRIPE_SECRET_KEY — ключ Stripe

STRIPE_PUBLISHABLE_KEY — публичный ключ Stripe

EMAIL_HOST_USER, EMAIL_HOST_PASSWORD — для отправки писем.


### 3. Запуск

```bash
docker-compose up --build
```

## Сервисы:

- API: http://localhost:8000

- Swagger: http://localhost:8000/swagger/

- ReDoc: http://localhost:8000/redoc/

- Admin: http://localhost:8000/admin/


### 4. Создание суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Остановка
```bash
docker-compose down
```

## С удалением данных:
```bash
docker-compose down -v
```

## Локальная разработка
```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Эндпоинты:
#### - Пользователи:

POST /api/users/register/ — регистрация

POST /api/users/login/ — вход

POST /api/users/token/ — JWT

GET /api/users/profile/ — профиль

GET /api/users/payments/ — платежи

#### - Курсы и уроки:
GET /api/courses/ — список курсов

POST /api/courses/ — создать курс

GET /api/lessons/ — список уроков

POST /api/lessons/ — создать урок

POST /api/subscriptions/ — подписка

#### - Платежи
POST /api/payments/create/ — создать оплату

GET /api/payments/success/ — успешная оплата

GET /api/payments/cancel/ — отмена

### Запуск:

```bash
docker-compose up --build