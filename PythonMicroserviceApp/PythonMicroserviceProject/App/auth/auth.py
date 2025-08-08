from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from App.config import API_TOKEN

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def verify_token(api_key: str = Security(api_key_header)):
    if api_key != API_TOKEN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Unauthorized"
        )
