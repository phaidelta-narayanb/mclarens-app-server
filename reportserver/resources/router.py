
from fastapi import FastAPI


def init_app(app: FastAPI):
    from . import (
        task,
        report,
        ws,
        utility,
    )

    task.init_app(app)
    report.init_app(app)
    ws.init_app(app)
    utility.init_app(app)
