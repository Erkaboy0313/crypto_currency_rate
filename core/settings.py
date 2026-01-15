from dotenv import load_dotenv
import os

load_dotenv()


DB_PASSWORD = os.getenv("DB_PASSWORD")  # Replace with your actual database password
DB_USER = os.getenv("DB_USER")      # Replace with your actual database username
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")      # Replace with your actual database name
DB_PORT = os.getenv("DB_PORT")                   # Default PostgreSQL port
REDIS_HOST = os.getenv("REDIS_HOST")


DATABASE_CONFIG = {
    "connections": {
        "default": f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",  # PostgreSQL connection string
        # "default": "sqlite://db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],  # Add your model paths here
            "default_connection": "default",
        }
    },
    "use_tz": True,  # If you want to use timezone-aware datetime fields
    "timezone": "Asia/Tashkent",  # Set your desired timezone
}