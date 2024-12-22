from functools import wraps
import json
import aioredis
import logging
from ..config import TESTING, REDIS_HOST, REDIS_PORT, REDIS_DB

logger = logging.getLogger(__name__)

# Initialize Redis client
redis_client = None
if not TESTING:
    try:
        redis_client = aioredis.from_url(
            f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            decode_responses=True
        )
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")

# Use in-memory cache for testing
IN_MEMORY_CACHE = {}

def cache_response(expire_time=300):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            try:
                key = f"{f.__name__}:{str(args)}:{str(kwargs)}"
                
                if TESTING:
                    # In test environment, use in-memory cache
                    if key in IN_MEMORY_CACHE:
                        return IN_MEMORY_CACHE[key]
                    
                    try:
                        result = await f(*args, **kwargs)
                        IN_MEMORY_CACHE[key] = result
                        return result
                    except Exception as e:
                        logger.error(f"Function error in testing: {e}")
                        raise  # Re-raise the exception without caching
                
                if redis_client:
                    try:
                        exists = await redis_client.exists(key)
                        if exists:
                            cached_data = await redis_client.get(key)
                            if cached_data:
                                return json.loads(cached_data)
                    except Exception as e:
                        logger.error(f"Redis error: {e}")
                
                result = await f(*args, **kwargs)
                
                if redis_client:
                    try:
                        await redis_client.setex(
                            key,
                            expire_time,
                            json.dumps(result)
                        )
                    except Exception as e:
                        logger.error(f"Failed to cache result: {e}")
                
                return result
            except Exception as e:
                logger.error(f"Cache decorator error: {e}")
                raise  # Re-raise the exception instead of calling the function again
            
        return decorated_function
    return decorator 