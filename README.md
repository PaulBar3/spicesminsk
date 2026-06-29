# Spices Minsk

Каталог специй и пряностей.

## Быстрый старт (локальная разработка)

```bash
# Установка зависимостей
uv sync --dev

# Копирование и настройка .env
cp .env.example .env

# Миграции
uv run python manage.py migrate

# Загрузка демо-данных
uv run python manage.py loaddata catalog/fixtures/demo.json

# Запуск dev-сервера
uv run python manage.py runserver
```

## Запуск через Docker (production-ready)

```bash
# Сборка и запуск всех сервисов (PostgreSQL + Redis + Django + Nginx)
docker compose up --build -d

# Миграции и создание суперпользователя выполняются автоматически
# через docker-entrypoint.sh
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `SECRET_KEY` | — | **Обязательно.** Секретный ключ Django |
| `DEBUG` | `False` | Режим отладки |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Разрешённые хосты (через запятую) |
| `ADMIN_URL` | `admin/` | Путь к админке (обфускация) |
| `DB_ENGINE` | `sqlite` | `sqlite` или `postgresql` |
| `DB_NAME` | `spicesminsk` | Название БД (только PostgreSQL) |
| `DB_USER` | `spicesminsk` | Пользователь БД (только PostgreSQL) |
| `DB_PASSWORD` | — | Пароль БД (только PostgreSQL) |
| `DB_HOST` | `localhost` | Хост БД (только PostgreSQL) |
| `DB_PORT` | `5432` | Порт БД (только PostgreSQL) |
| `REDIS_URL` | — | URL Redis для кэширования (например `redis://redis:6379/0`) |
| `SENTRY_DSN` | — | DSN Sentry для отслеживания ошибок |
| `SECURE_SSL_REDIRECT` | `False` | Принудительный HTTPS |
| `LOG_LEVEL` | `INFO` | Уровень логирования |
| `WEB_CONCURRENCY` | `2*CPU+1` | Количество воркеров gunicorn |

Полный список — в `.env.example`.

## Deploy

### Минимальные требования

- Docker и Docker Compose
- Reverse proxy с TLS (например, Caddy, Traefik, nginx + certbot)

### Рекомендации по продакшену

1. Сгенерируйте уникальный `SECRET_KEY`
2. Установите `DEBUG=False`
3. Укажите домен в `ALLOWED_HOSTS`
4. Используйте `DB_ENGINE=postgresql` с PostgreSQL
5. Настройте `REDIS_URL` для кэширования
6. Настройте HTTPS через reverse proxy
7. Опционально: подключите Sentry через `SENTRY_DSN`

### Health check

```
GET /health/ → {"status": "ok"}
```

Используется для проверки работоспособности при оркестрации (Kubernetes, Docker healthcheck и т.д.).
