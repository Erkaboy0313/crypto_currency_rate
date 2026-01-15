# Crypto Price Tracker API

Проект автоматически получает цены BTC и ETH с криптобиржи Deribit каждую минуту, сохраняет их в базу данных PostgreSQL и предоставляет HTTP API на FastAPI для получения последней цены, всей истории и данных за указанный период. Периодический сбор данных реализован с помощью Celery и Celery Beat.

## Технологический стек

- Python 3.11+
- FastAPI
- Tortoise ORM + Aerich
- PostgreSQL
- Redis
- Celery + Celery Beat
- aiohttp (асинхронные HTTP-запросы)

## Как запустить

1. Создайте файл `.env` на основе `.env.example` и при необходимости измените значения:

    ```bash
    cp .env.example .env
    ```

2. Инициализация базы данных (только при первом запуске):

    ```bash
    docker exec -it api aerich init -t core.settings.DATABASE_CONFIG
    docker exec -it api aerich init-db
    ```

3. Запустите все сервисы с помощью Docker Compose:

    ```bash
    docker-compose up --build
    ```

    Будут запущены:

    - FastAPI API
    - Celery worker
    - Celery Beat
    - Redis
    - PostgreSQL

4. Для будущих изменений моделей и миграций:

    ```bash
    docker exec -it api aerich migrate
    docker exec -it api aerich upgrade
    ```

После этого проект полностью готов к работе.

## Решения по архитектуре

- **Структура проекта:** Django-подобная структура с разделением на apps и четким разделением ответственности
- **Периодические задачи:** Celery + Celery Beat для надежного планирования задач
- **Асинхронность:** aiohttp и асинхронный Tortoise ORM для эффективной работы с I/O
- **Валидация:** Pydantic-схемы и Enum для строгой валидации query-параметров
- **Чистая архитектура:** API слой не содержит бизнес-логики, вся логика вынесена в сервисы
- **Конфигурация:** Все настройки берутся из `.env`
- **Логирование:** Используется стандартный logging вместо print

## API Эндпоинты

- **GET /prices/latest?ticker=BTC_USD** — возвращает последнюю сохранённую цену валюты
- **GET /prices/history?ticker=BTC_USD** — возвращает всю историю цен по валюте
- **GET /prices/range?ticker=BTC_USD&start=UNIX&end=UNIX** — возвращает цены за указанный диапазон дат (UNIX timestamp)
