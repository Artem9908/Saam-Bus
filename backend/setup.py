from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1",
    packages=find_packages(include=['app', 'app.*']),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "redis",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
    ],
    python_requires=">=3.9",
) 