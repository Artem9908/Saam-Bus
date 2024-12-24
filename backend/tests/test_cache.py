import pytest
from redis import Redis
import json
import asyncio
from app.services.document import DocumentService
from datetime import datetime
from app.services.cache import RedisCache, cache_response
from app.config import TESTING, REDIS_HOST, REDIS_PORT
from app.services.cache_decorator import IN_MEMORY_CACHE, cache_response

@pytest.fixture
def test_redis_client():
    """Create a test Redis client"""
    if TESTING:
        pytest.skip("Skipping Redis tests in test environment")
    return Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        decode_responses=True
    )

@pytest.fixture
def cache():
    return RedisCache(host='localhost', port=6379)

def cache_document(expire_time: int = 300):
    """Decorator for caching document responses"""
    return cache_response(expire_time=expire_time)

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear the cache before each test"""
    IN_MEMORY_CACHE.clear()
    yield

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
    assert result2["count"] == 1  # Should be same as first call
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
    assert result2["count"] == 1  # Should be cached
    assert result3["count"] == 2  # Different args = new cache entry

def test_cache_disabled_in_testing():
    """Verify that caching is effectively disabled in test environment"""
    from app.services.cache import RedisCache
    from app.config import TESTING

    assert TESTING is True
    cache = RedisCache()
    assert cache._cache == {}, "In-memory cache should be empty"
    assert cache.redis is None, "Redis client should be None in test environment"

@pytest.mark.skipif(TESTING, reason="Skip Redis tests in test environment")
def test_redis_connection(test_redis_client):
    """Test Redis connection when not in test environment"""
    assert test_redis_client.ping()

@pytest.mark.asyncio
async def test_cache_response(test_db):
    """Test that caching works correctly"""
    
    @cache_response(expire_time=1)
    async def test_cached_function(db):
        return {
            "timestamp": datetime.now().isoformat(),
            "data": "test"
        }
    
    # First call
    result1 = await test_cached_function(test_db)
    # Second call should return cached result
    result2 = await test_cached_function(test_db)
    
    assert result1 == result2

@pytest.mark.asyncio
async def test_document_list_caching(async_client, test_db):
    """Test document listing endpoint caching"""
    # First request
    response1 = await async_client.get("/documents")
    assert response1.status_code == 200
    
    # Second request should return cached result
    response2 = await async_client.get("/documents")
    assert response2.status_code == 200
    assert response1.json() == response2.json()

@pytest.mark.asyncio
async def test_document_cache(document_service, test_db):
    """Test document caching"""
    cache = RedisCache()
    await cache.clear()
    
    # Create test document
    doc_data = {
        "name": "Test Doc",
        "date": "2024-01-01",
        "amount": 100.50,
        "template_type": "receipt"
    }
    
    # Test caching
    result1 = await document_service.generate_document_content(**doc_data)
    result2 = await document_service.generate_document_content(**doc_data)
    
    assert result1 == result2

@pytest.mark.asyncio
async def test_cache_expiration():
    """Test cache expiration"""
    cache = RedisCache()
    
    # Set with short expiration
    await cache.set("test_key", "test_value", expire_time=1)
    
    # Immediate get should return value
    assert await cache.get("test_key") == "test_value"
    
    # Wait for expiration
    await asyncio.sleep(1.1)
    
    # Should return None after expiration
    assert await cache.get("test_key") is None

@pytest.mark.asyncio
async def test_document_cache_operations():
    """Test document cache operations"""
    cache = RedisCache()
    test_doc = {
        "id": "test-123",
        "name": "Test Doc",
        "content": "Test content"
    }
    
    # Test setting document
    await cache.set_document("test-123", test_doc)
    
    # Test getting document
    cached_doc = await cache.get_document("test-123")
    assert cached_doc == test_doc
    
    # Test invalidating document
    await cache.invalidate_document("test-123")
    assert await cache.get_document("test-123") is None

@pytest.mark.asyncio
async def test_cache_behavior_in_testing():
    """Test that in-memory caching works in testing mode"""
    counter = 0
    IN_MEMORY_CACHE.clear()

    @cache_response(expire_time=60)
    async def test_func():
        nonlocal counter
        counter += 1
        return counter

    result1 = await test_func()
    result2 = await test_func()

    assert result1 == 1
    assert result2 == 1  # Should be cached
    assert counter == 1  # Function should only be called once