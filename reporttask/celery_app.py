import os

from celery import Celery
from .config import CelerySettings


settings = CelerySettings()

print(settings.backend_dsn)
print(settings.broker_dsn)

app = Celery(
    __name__,
    broker=str(settings.broker_dsn),
    backend=str(settings.backend_dsn),
    include=[".".join([__package__, "tasks"])],
)
