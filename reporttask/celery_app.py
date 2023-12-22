from celery import Celery
from .config import CelerySettings

settings = CelerySettings()

app = Celery(
    __name__,
    broker=str(settings.broker_dsn),
    backend=str(settings.backend_dsn),
    include=[".".join([__package__, "tasks"])],
)
