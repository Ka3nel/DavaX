from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader
from App.db.database import init_db
from App.api.routes import router
from App.logger.logger import setup_logging
from App.config import API_TOKEN

# Declare the security scheme
api_key_header = APIKeyHeader(name="Authorization")

app = FastAPI(
    title="Math Microservice API",
    version="0.1.0",
    openapi_tags=[{"name": "default", "description": "Math operations"}],
    swagger_ui_parameters={"persistAuthorization": True}
)

setup_logging()
init_db()
app.include_router(router)
print(API_TOKEN)