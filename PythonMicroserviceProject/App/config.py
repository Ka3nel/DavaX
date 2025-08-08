from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

API_TOKEN = os.getenv("API_TOKEN", "default-token")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./math_ops.db")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
CACHE_TTL = int(os.getenv("CACHE_TTL", "60"))
