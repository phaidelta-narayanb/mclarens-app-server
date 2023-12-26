
from .celery_app import app


@app.task(name="my_task")
def abc():
    pass
