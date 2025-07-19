# 📚 Papyrus

Проект для управления каталогом книг с использованием FastAPI, SQLAlchemy, Alembic и PostgreSQL.

## ⚙️ Переменные окружения

Перед запуском необходимо задать следующие переменные окружения:

`POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=papyrus`

## 📦 Установка зависимостей

Установите зависимости командой:

`poetry install`

## 🐘 Запуск базы данных

Для запуска PostgreSQL используйте Docker Compose:

`docker compose up -d`

## 🧱 Применение миграций

После запуска базы данных выполните миграции:

`PYTHONPATH=src alembic -c src/library_catalog/alembic.ini upgrade head`

## Запустите сервер командой:

`python3 src/library_catalog/manage.py`


## 🌐 Доступ к приложению

Проект будет доступен по адресу:

http://localhost:8000/docs
