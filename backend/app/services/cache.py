from typing import Optional, Any
import logging
from redis import asyncio as aioredis
from datetime import datetime
from ..config import REDIS_HOST, REDIS_PORT, REDIS_DB, TESTING
import json
from .cache_decorator import cache_response
import time

logger = logging.getLogger(__name__)

# In-memory cache for testing
IN_MEMORY_CACHE = {}
redis_client = None

class RedisCache:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.redis = None
        self.host = host
        self.port = port
        self._cache = {}
        self._expiry = {}

    async def initialize(self):
        """Initialize Redis connection"""
        if not TESTING and not self.redis:
            try:
                self.redis = await aioredis.Redis(
                    host=self.host,
                    port=self.port,
                    decode_responses=True
                ).initialize()
            except Exception as e:
                logger.error(f"Redis connection error: {e}")
                # Fallback to in-memory cache
                self.redis = None

    async def get(self, key: str) -> Optional[str]:
        """Get cache entry"""
        try:
            if TESTING:
                return self._cache.get(key)
            else:
                if self.redis:
                    return await self.redis.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None

    async def set(self, key: str, value: str, expire_time: int = 300):
        """Set cache entry"""
        try:
            if TESTING:
                self._cache[key] = value
                self._expiry[key] = time.time() + expire_time
            else:
                if self.redis:
                    await self.redis.set(key, value, ex=expire_time)
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    async def set_document(self, doc_id: str, document: dict):
        """Set document in cache"""
        key = f"doc:{doc_id}"
        await self.set(key, json.dumps(document))

    async def get_document(self, doc_id: str) -> Optional[dict]:
        """Get document from cache"""
        key = f"doc:{doc_id}"
        cached = await self.get(key)
        return json.loads(cached) if cached else None

    async def delete(self, key: str):
        """Delete cache entry"""
        try:
            if TESTING:
                self._cache.pop(key, None)
            else:
                await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

    async def clear(self):
        """Clear all cache entries"""
        if TESTING:
            self._cache.clear()
        else:
            try:
                await self.redis.flushall()
            except Exception as e:
                logger.error(f"Redis clear error: {e}")

    def _get_cache_key(self, method_name: str, *args, **kwargs) -> str:
        """Generate a cache key from method name and arguments"""
        key_parts = [method_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return ":".join(key_parts)

    @cache_response(expire_time=300)
    async def get_documents(self, *args, **kwargs):
        """Cache wrapper for document listing"""
        # This is just a placeholder - the actual implementation 
        # will be provided by the document service
        pass

    async def invalidate_document(self, doc_id: str):
        """Remove document from cache"""
        key = f"doc:{doc_id}"
        await self.delete(key)