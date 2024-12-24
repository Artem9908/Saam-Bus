from typing import Dict
import redis
from sqlalchemy import text
from ..database import engine
from ..config import REDIS_HOST, REDIS_PORT
from .google_drive import GoogleDriveService

async def check_db_connection() -> Dict[str, bool]:
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return {"status": True}
    except Exception as e:
        return {"status": False, "error": str(e)}

async def check_redis_connection() -> Dict[str, bool]:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.ping()
        return {"status": True}
    except Exception as e:
        return {"status": False, "error": str(e)}

async def check_google_api() -> Dict[str, bool]:
    try:
        service = GoogleDriveService()
        if service.service is not None:
            return {"status": True}
        return {"status": False, "error": "Service not initialized"}
    except Exception as e:
        return {"status": False, "error": str(e)} 