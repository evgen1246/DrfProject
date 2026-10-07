# DrfProject

LMS-платформа с курсами, уроками и платежами через Stripe.  
Backend на Django REST Framework, развёрнут на удалённом сервере с Docker, Nginx и CI/CD через GitHub Actions.

**Production:** http://158.160.240.116/admin/

---

## Стек

- Python 3.12
- Django 5.2, Django REST Framework
- PostgreSQL 16
- Redis 7
- Celery + Celery Beat
- JWT (SimpleJWT)
- Stripe API
- Docker + Docker Compose
- Nginx (reverse proxy)
- GitHub Actions (CI/CD)
- Poetry (управление зависимостями)

---

## Возможности

- Регистрация и аутентификация пользователей (JWT)
- Управление курсами и уроками
- Подписки на курсы
- Оплата через Stripe
- Асинхронные задачи (Celery): рассылки, блокировка неактивных пользователей
- Периодические задачи (Celery Beat)
- Swagger / ReDoc документация API
- Админка Django

---

## Быстрый старт (локально через Docker)

### 1. Клонирование

```bash
git clone https://github.com/evgen1246/DrfProject.git
cd DrfProject
```

### 2. Настройка окружения

```bash
cp .env.sample .env
```

Заполните `.env`:

| Переменная | Описание |
|---|---|
| `SECRET_KEY` | секретный ключ Django |
| `DEBUG` | `True` для разработки, `False` для прода |
| `ALLOWED_HOSTS` | через запятую: `localhost,127.0.0.1` |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | доступы к БД |
| `POSTGRES_HOST` | `localhost` локально, `db` в Docker |
| `POSTGRES_PORT` | `5432` |
| `REDIS_HOST` | `localhost` локально, `redis` в Docker |
| `REDIS_PORT` | `6379` |
| `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` | ключи Stripe |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | для отправки писем |

### 3. Запуск

```bash
docker compose up --build
```

Приложение доступно:
- API: http://localhost:8000
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Admin: http://localhost:8000/admin/

### 4. Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Остановка

```bash
docker compose down          # сохранив данные
docker compose down -v       # с удалением volume'ов
```

---

## Локальная разработка (без Docker)

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

Требуется локально установленный PostgreSQL и Redis с настройками из `.env`.

---

## Production на сервере

**URL:** http://158.160.240.116/admin/  
**Сервер:** Yandex Cloud, Ubuntu 24.04

### Архитектура

6 сервисов в `docker-compose.prod.yml`:

| Сервис | Назначение |
|---|---|
| `web` | Django + Gunicorn (3 воркера) |
| `db` | PostgreSQL 16 |
| `redis` | Брокер сообщений для Celery |
| `celery_worker` | Выполнение фоновых задач |
| `celery_beat` | Периодические задачи |
| `nginx` | Reverse proxy, отдача статики и медиа |

### Безопасность

- Все секреты в `.env` (не в Git, добавлен в `.gitignore`)
- `.env.sample` — публичный шаблон без секретов
- SSH deploy-key для GitHub Actions (отдельный от пользовательского)
- Firewall (`ufw` + Security Group Yandex Cloud): открыты только 22, 80, 443
- PostgreSQL и Redis доступны только внутри docker-сети
- `DEBUG=False` на проде

### Ручной деплой

```bash
ssh -l evgen1246 158.160.240.116
cd ~/drfproject
git pull origin develop
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```

---

## CI/CD

Pipeline на GitHub Actions (`.github/workflows/deploy.yml`):

```
lint → test → build → deploy
```

| Этап | Что делает |
|---|---|
| **lint** | `black --check`, `isort --check-only` |
| **test** | `python manage.py test` на SQLite в чистом окружении |
| **build** | `docker build -f Dockerfile.prod` — проверка сборки образа |
| **deploy** | SSH на сервер, `git pull`, `docker compose up -d --build`, `migrate` |

### Триггеры

- **push** в `develop` → все 4 этапа
- **pull_request** в `develop`/`main` → только lint + test (деплой не запускается)
- Деплой выполняется **только** при успешном прохождении lint, test и build

### GitHub Secrets

| Secret | Значение |
|---|---|
| `SSH_HOST` | IP сервера (`158.160.240.116`) |
| `SSH_USER` | `evgen1246` |
| `SSH_KEY` | приватный deploy-ключ (ed25519) |
| `SSH_PORT` | `22` |
| `DJANGO_SECRET_KEY` | секрет для тестов в CI |

### Как работает деплой

1. Developer пушит в `develop`
2. GitHub Actions запускает pipeline (lint → test → build)
3. Если все этапы зелёные — job `deploy` подключается к серверу по SSH
4. На сервере выполняются: `git pull`, `docker compose up -d --build`, `migrate`
5. Через ~1–2 минуты изменения на проде

---

## API эндпоинты

### Пользователи (`/api/users/`)

| Метод | URL | Описание |
|---|---|---|
| POST | `/register/` | регистрация |
| POST | `/login/` | вход |
| POST | `/token/` | получить JWT-токен |
| GET | `/profile/` | профиль пользователя |
| GET | `/payments/` | платежи пользователя |

### Курсы и уроки (`/api/`)

| Метод | URL | Описание |
|---|---|---|
| GET | `/courses/` | список курсов |
| POST | `/courses/` | создать курс |
| GET | `/lessons/` | список уроков |
| POST | `/lessons/` | создать урок |
| POST | `/subscriptions/` | подписка на курс |

### Платежи (`/api/payments/`)

| Метод | URL | Описание |
|---|---|---|
| POST | `/create/` | создать оплату через Stripe |
| GET | `/success/` | успешная оплата |
| GET | `/cancel/` | отмена оплаты |

---

## Структура проекта

```
DrfProject/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── config/                      # настройки Django, celery, urls, wsgi
│   ├── settings.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
├── users/                       # пользователи, аутентификация, задачи
│   ├── models.py
│   ├── tasks.py
│   └── ...
├── learnix/                     # курсы, уроки, подписки
├── payments/                    # интеграция со Stripe
├── nginx/
│   └── nginx.conf               # конфиг reverse proxy
├── Dockerfile                   # dev-сборка
├── Dockerfile.prod              # production-сборка (gunicorn)
├── docker-compose.yml           # dev-конфиг
├── docker-compose.prod.yml      # production-конфиг (6 сервисов)
├── pyproject.toml               # зависимости (poetry)
├── poetry.lock
├── manage.py
├── .env.sample                  # шаблон окружения
└── README.md
```

---

## Полезные команды

### Логи сервисов

```bash
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f celery_worker
docker compose -f docker-compose.prod.yml logs -f nginx
```

### Перезапуск конкретного сервиса

```bash
docker compose -f docker-compose.prod.yml restart web
```

### Полная пересборка

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
```

### Проверка статуса

```bash
docker compose -f docker-compose.prod.yml ps
```

---

