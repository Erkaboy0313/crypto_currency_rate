from core.celery_app import celery_app
from .services import fetch_and_store_prices
from .logger import logger
from tortoise import run_async

@celery_app.task(
    name="app.tasks.fetch_prices",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def fetch_prices(self):
    try:
        run_async(fetch_and_store_prices())
    except Exception as exc:
        logger.error(f"Task failed: {exc}")
        raise self.retry(exc=exc)