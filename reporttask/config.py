from pydantic import AnyUrl, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    broker_dsn: AnyUrl = RedisDsn("redis://localhost:6379/0")
    '''Connection string to the message broker service'''

    backend_dsn: AnyUrl = RedisDsn("redis://localhost:6379/0")
    '''Connection string to the task result storage service'''

    model_config = SettingsConfigDict(
        secrets_dir="secrets/",
        env_prefix="CELERY_",
        env_file=".env",
    )
