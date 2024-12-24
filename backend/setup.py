from setuptools import setup, find_packages

setup(
    name="document-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "redis",
        "google-api-python-client",
        "google-auth",
        "pytest",
        "pytest-asyncio",
        "httpx"
    ]
)