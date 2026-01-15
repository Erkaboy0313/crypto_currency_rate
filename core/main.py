from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .settings import DATABASE_CONFIG
from app.api import router as prices_router
app = FastAPI()


app.include_router(prices_router)

register_tortoise(
    app,
    config=DATABASE_CONFIG,
    generate_schemas=True,  
    add_exception_handlers=True,  
)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to confirm that the API is running.
    """
    return {"status": "ok", "detail": "API is running"}
