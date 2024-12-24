from prometheus_client import Counter, Histogram, CollectorRegistry
import time
from functools import wraps
from typing import Dict
import psutil
from collections import defaultdict
import logging

# Create a custom registry
registry = CollectorRegistry()

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['path', 'method', 'status'],
    registry=registry
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['path'],
    registry=registry
)

DOCUMENT_GENERATION_COUNT = Counter(
    'document_generation_total',
    'Total number of documents generated',
    registry=registry
)

GOOGLE_API_LATENCY = Histogram(
    'google_api_latency_seconds',
    'Google API request duration in seconds',
    registry=registry
)

# Request tracking
request_times = defaultdict(list)
request_counts = defaultdict(int)
error_counts = defaultdict(int)

def record_request_metric(method: str, endpoint: str, status_code: int, duration: float):
    """Record request metrics"""
    REQUEST_COUNT.labels(
        path=endpoint,
        method=method,
        status=str(status_code)
    ).inc()
    
    REQUEST_LATENCY.labels(
        path=endpoint
    ).observe(duration)

def generate_metrics() -> Dict:
    """Generate service metrics"""
    metrics = {
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
        },
        "application": {
            "total_requests": sum(request_counts.values()),
            "average_response_time": 0.0,
            "error_rate": 0.0,
            "endpoints": {}
        }
    }
    
    # Calculate application-wide metrics
    total_duration = sum(sum(times) for times in request_times.values())
    total_requests = sum(request_counts.values())
    total_errors = sum(error_counts.values())
    
    if total_requests > 0:
        metrics["application"]["average_response_time"] = total_duration / total_requests
        metrics["application"]["error_rate"] = (total_errors / total_requests) * 100
    
    # Calculate per-endpoint metrics
    for endpoint in request_counts:
        avg_response_time = sum(request_times[endpoint]) / len(request_times[endpoint])
        error_rate = (error_counts[endpoint] / request_counts[endpoint]) * 100 if request_counts[endpoint] > 0 else 0
        
        metrics["application"]["endpoints"][endpoint] = {
            "total_requests": request_counts[endpoint],
            "average_response_time_ms": round(avg_response_time * 1000, 2),
            "error_rate_percent": round(error_rate, 2)
        }
    
    return metrics

def track_latency(metric):
    """Decorator to track latency of a function"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                metric.observe(time.time() - start_time)
        return wrapper
    return decorator

# Export all necessary components
__all__ = [
    'REQUEST_COUNT',
    'REQUEST_LATENCY',
    'DOCUMENT_GENERATION_COUNT',
    'GOOGLE_API_LATENCY',
    'record_request_metric',
    'generate_metrics',
    'track_latency'
] 