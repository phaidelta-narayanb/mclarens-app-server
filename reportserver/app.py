from typing import Any, Mapping
from jinja2 import Environment, FileSystemLoader

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .resources import router as app_router
from .reportgen.report_export import ReportExporter
from .reportgen.report_maker import ReportMaker
from .config import Settings


API_VERSION = "0.1.9"
"""Protocol version"""

# FIXME: Change to proper domains and load from config file, remove this once done
CORS_ALLOWED_ORIGINS = [
    "*",
]
"""Cross-Origin allowed domains"""


def app_config() -> Mapping[str, Any]:
    # settings = Settings()

    # TODO: Get these from the settings object
    return dict(
        version=API_VERSION,
        description="Server for Report logic for Mclarens Application",
        cors_allowed_origins=CORS_ALLOWED_ORIGINS,
        report_maker=ReportMaker(
            template_env=Environment(
                loader=FileSystemLoader("templates/"), enable_async=True
            )
        ),
        report_exporter=ReportExporter(
            "weasyprint",
            input_format="html",
        ),
    )


def init_app():
    app = FastAPI(**app_config())

    app_router.init_app(app)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=app.extra.get("cors_allowed_origins", ["*"]),
        allow_methods=app.extra.get("cors_allowed_methods", ["*"]),
        allow_headers=app.extra.get("cors_allowed_headers", ["*"]),
    )

    return app


def serve():
    """Serve the application - for development use. Use Gunicorn with `init_app` directly for production"""
    import uvicorn

    uvicorn.run(init_app, factory=True)
