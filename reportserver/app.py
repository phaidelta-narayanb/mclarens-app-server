import asyncio
import logging
from pathlib import Path
from typing import Any, Mapping, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader
from tortoise import Tortoise

from reportgen.report_export import ReportExporter
from reportgen.report_maker import ReportMaker
from reportserver.db.config import AppModule, DBSettings
from reportserver.utils import app_init_config, unhandled_exception_handler

from .config import Settings  # noqa, TODO
from .resources import router as app_router

LOG = logging.getLogger()

API_VERSION = "0.2.0"
"""Protocol version"""

# FIXME: Change to proper domains and load from config file, remove this once done
CORS_ALLOWED_ORIGINS = [
    "*",
]
"""Cross-Origin allowed domains"""


# TODO: Use BaseModel for storing config
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
        db_settings=DBSettings(
            connections=dict(default="sqlite://dummy.dev.db"),
            apps={
                __package__: AppModule(
                    models=[
                        ".".join([__package__, "resources", "register_db_models"])
                    ]
                )
            },
        ),  # TODO: Get from `settings` field
    )


@app_init_config
def init_app(config: Optional[Mapping[str, Any]] = None) -> FastAPI:
    """App factory method to create and initialize a new FastAPI application"""
    if config is None:
        config = app_config()

    # Initialize new application with configuration
    app = FastAPI(**config)

    # Apply all routes defined in `resources`
    app_router.init_app(app)

    # Exception handler "middlewares" (only executed when Exceptions occur)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=app.extra.get("cors_allowed_origins", ["*"]),
        allow_methods=app.extra.get("cors_allowed_methods", ["*"]),
        allow_headers=app.extra.get("cors_allowed_headers", ["*"]),
    )

    return app


async def init_db_async(db_settings: DBSettings):
    LOG.info("Initializing database...")
    await Tortoise.init(config=db_settings.model_dump(mode="json"))

    # Generate the schema
    LOG.info("Generating database schema.")
    await Tortoise.generate_schemas()
    LOG.info("Database initialization completed.")


def init_db(config: Optional[Mapping[str, Any]] = None):
    """Initialize the database from the given configuration"""
    if config is None:
        config = app_config()

    asyncio.run(init_db_async(config["db_settings"]))


def serve():
    """Serve the application - for development use. Use Gunicorn with `init_app` directly for production"""
    import uvicorn

    from .utils import init_logger

    # Initialize logger from config file
    init_logger(Path("logging.dev.ini"))

    # Configuration used for initializing db and application
    config = app_config()

    # Initialize database
    init_db(config)

    app_fact = init_app(config=config)

    # Create app with configuration
    uvicorn.run(app_fact, factory=True)
