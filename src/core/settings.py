import os
from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    KAFKA_DSN: str = os.environ.get("KAFKA_DSN", "0.0.0.0:9092")
    KAFKA_TOPIC_PREFIX: str = os.environ.get("KAFKA_TOPIC_PREFIX", "local.auth")
    REDIS_URL: RedisDsn = os.environ.get("REDIS_URL", "redis://localhost:6382")
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.environ.get("REDIS_PORT", 6382)

    JAEGER_ENABLED: bool = os.environ.get("JAEGER_ENABLED", True)
    JAEGER_HOST: str = os.environ.get("JAEGER_HOST", "0.0.0.0")
    JAEGER_PORT = os.environ.get("JAEGER_PORT", 6831)


settings = Settings()
