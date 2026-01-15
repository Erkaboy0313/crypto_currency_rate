# core/celery_app.py
from celery import Celery
from celery.schedules import crontab
from .settings import REDIS_HOST,DATABASE_CONFIG
from tortoise import run_async, Tortoise

def create_celery():
    celery_app = Celery(
        "core",
        broker=f"redis://{REDIS_HOST}:6379/0",
        include=["app.tasks"],  # register tasks
    )

    run_async(Tortoise.init(config=DATABASE_CONFIG))
    run_async(Tortoise.generate_schemas())

    # Celery Beat schedule
    celery_app.conf.beat_schedule = {
        "fetch-prices-every-minute": {
            "task": "app.tasks.fetch_prices",
            "schedule": crontab(minute="*"),  # every 60 seconds
        }
    }
    celery_app.conf.timezone = "UTC"

    return celery_app


celery_app = create_celery()
