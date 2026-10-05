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



docker-compose up --build

## CI/CD

Проект использует GitHub Actions для автоматизации:

- **Тесты** запускаются при каждом push и pull request в `develop`/`main`
- **Деплой на сервер** происходит автоматически после успешных тестов при push в `develop`

Файл конфигурации: `.github/workflows/deploy.yml`

### Как работает деплой
1. GitHub Actions подключается к серверу по SSH (ключ в secrets)
2. Выполняет `git pull`, `docker compose up -d --build`, `migrate`
3. Через ~1 минуту изменения на проде


### Production инфраструктура
- Добавлен `Dockerfile.prod` с Gunicorn
- Добавлен `docker-compose.prod.yml` (6 сервисов: web, db, redis, celery_worker, celery_beat, nginx)
- Настроен `nginx/nginx.conf` — reverse proxy + отдача статики/медиа
- Приложение работает на удалённом сервере Yandex Cloud (Ubuntu 24.04)

### Безопасность
- Все секреты вынесены в `.env` (не в Git)
- `.env.sample` — полный шаблон для разработки
- SSH-доступ через отдельный deploy-key
- Firewall: открыты только 22, 80, 443
- БД и Redis не доступны снаружи

### CI/CD (GitHub Actions)
- Workflow `.github/workflows/deploy.yml`
- Этапы: lint → test → build → deploy
- Тесты на SQLite (изолированно)
- Деплой по SSH только при push в `develop` после успешных тестов
- Секреты в GitHub Secrets: `SSH_HOST`, `SSH_USER`, `SSH_KEY`, `SSH_PORT`, `DJANGO_SECRET_KEY`

### Как запустить локально
1. `git clone -b develop https://github.com/evgen1246/DrfProject.git`
2. `cd DrfProject`
3. `cp .env.sample .env` — заполнить значения
4. `poetry install`
5. `poetry run python manage.py migrate`
6. `poetry run python manage.py runserver`

### Как задеплоить на сервер
Автоматически через GitHub Actions при push в `develop`.
Вручную:
```bash
ssh -l evgen1246 158.160.205.146
cd ~/drfproject
git pull
docker compose -f docker-compose.prod.yml up -d --build
```
