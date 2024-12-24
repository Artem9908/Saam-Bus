from functools import wraps
import json
import logging
from typing import Any, Callable
from ..config import TESTING
import time
from ..models import GeneratedDocument

logger = logging.getLogger(__name__)

# Global in-memory cache (moved from cache.py)
IN_MEMORY_CACHE = {}

def cache_response(expire_time: int = 300):
    """Cache decorator for API responses"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Use in-memory cache for testing
            if TESTING:
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                if cache_key in IN_MEMORY_CACHE:
                    return IN_MEMORY_CACHE[cache_key]
                
                response = await func(*args, **kwargs)
                # Serialize GeneratedDocument objects before caching
                if isinstance(response, dict) and "items" in response:
                    cached_response = {
                        **response,
                        "items": [item.to_dict() if isinstance(item, GeneratedDocument) else item 
                                for item in response["items"]]
                    }
                else:
                    cached_response = response
                    
                IN_MEMORY_CACHE[cache_key] = cached_response
                return response
            
            try:
                # Get cache instance and ensure it's initialized
                from .cache import RedisCache
                cache = RedisCache()
                await cache.initialize()
                
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                cached_response = await cache.get(cache_key)
                
                if cached_response:
                    return json.loads(cached_response)
                
                response = await func(*args, **kwargs)
                
                # Serialize response before caching
                if isinstance(response, dict) and "items" in response:
                    cached_response = {
                        **response,
                        "items": [item.to_dict() if hasattr(item, 'to_dict') else item 
                                for item in response["items"]]
                    }
                else:
                    cached_response = response
                    
                await cache.set(cache_key, json.dumps(cached_response), expire_time)
                return response
                
            except Exception as e:
                logger.error(f"Cache error: {e}")
                return await func(*args, **kwargs)
                
        return wrapper
    return decorator