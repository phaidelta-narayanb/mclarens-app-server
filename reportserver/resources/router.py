
from fastapi import FastAPI


def init_app(app: FastAPI):
    from . import (
        report,
        utility
    )

    report.init_app(app)
    utility.init_app(app)
