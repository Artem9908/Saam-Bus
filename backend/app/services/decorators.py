from functools import wraps
import json
import logging
from typing import Any, Callable
from .cache_decorator import IN_MEMORY_CACHE  # Import from cache_decorator instead

logger = logging.getLogger(__name__)

def cache_response(expire_time: int = 300):
    """Cache decorator for API responses"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if TESTING:
                # Use in-memory cache for testing
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                if cache_key in IN_MEMORY_CACHE:
                    return IN_MEMORY_CACHE[cache_key]
                
                result = await func(*args, **kwargs)
                IN_MEMORY_CACHE[cache_key] = result
                return result

            # Normal Redis caching logic for production
            try:
                self = args[0]  # Get instance from method call
                cache_key = self._get_cache_key(func.__name__, *args[1:], **kwargs)
                
                cached_response = await self.get(cache_key)
                if cached_response:
                    return json.loads(cached_response)
                
                response = await func(*args, **kwargs)
                await self.set(cache_key, json.dumps(response), expire_time)
                return response
                
            except Exception as e:
                logger.error(f"Cache error: {e}")
                return await func(*args, **kwargs)
                
        return wrapper
    return decorator