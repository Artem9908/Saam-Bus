import pytest
from fastapi.testclient import TestClient
import redis
import aioredis
from app.main import app
from app.config import TESTING, REDIS_HOST, REDIS_PORT
from app.services.cache import cache_response, IN_MEMORY_CACHE, redis_client
import json
import asyncio

@pytest.fixture
def test_redis_client():
    """Create a test Redis client"""
    if TESTING:
        pytest.skip("Skipping Redis tests in test environment")
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )

@pytest.mark.asyncio
async def test_cache_decorator():
    """Test cache decorator in test environment"""
    counter = 0
    IN_MEMORY_CACHE.clear()  # Clear cache before test
    
    @cache_response(expire_time=60)
    async def test_func():
        nonlocal counter
        counter += 1
        return {"data": "test", "count": counter}
    
    # First call
    result1 = await test_func()
    assert result1["count"] == 1
    
    # Second call (should use cached value)
    result2 = await test_func()
    assert result2["count"] == 1  # Should be 1, not 2, because we're using cache
    assert counter == 1  # Function should only be called once

@pytest.mark.asyncio
async def test_cache_decorator_with_error():
    """Test cache decorator when an error occurs"""
    counter = 0
    IN_MEMORY_CACHE.clear()

    @cache_response(expire_time=60)
    async def test_func_error():
        nonlocal counter
        counter += 1
        raise Exception("Test error")

    # Should handle the error and not cache the error result
    with pytest.raises(Exception):
        await test_func_error()
    
    # The function should be called exactly once
    assert counter == 1
    assert len(IN_MEMORY_CACHE) == 0  # Error results should not be cached

@pytest.mark.asyncio
async def test_cache_with_different_args():
    """Test cache with different arguments"""
    counter = 0
    IN_MEMORY_CACHE.clear()

    @cache_response(expire_time=60)
    async def test_func_args(arg1, arg2=None):
        nonlocal counter
        counter += 1
        return {"arg1": arg1, "arg2": arg2, "count": counter}

    # Test with different arguments
    result1 = await test_func_args("test1", arg2="value1")
    result2 = await test_func_args("test1", arg2="value1")  # Same args
    result3 = await test_func_args("test2", arg2="value2")  # Different args

    assert result1["count"] == 1
    assert result2["count"] == 1  # Should use cache
    assert result3["count"] == 2  # Should not use cache
    assert counter == 2

def test_cache_disabled_in_testing():
    """Verify that caching is disabled in test environment"""
    assert TESTING is True, "TESTING should be True in test environment"
    assert redis_client is None, "Redis client should be None in test environment"

@pytest.mark.skipif(TESTING, reason="Skip Redis tests in test environment")
def test_redis_connection(test_redis_client):
    """Test Redis connection when not in test environment"""
    assert test_redis_client.ping()