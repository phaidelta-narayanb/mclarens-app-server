import functools
import logging
import logging.config
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

LOG = logging.getLogger()

EXCEPTION_MESSAGE_FORMAT = (
    '"{exception_name}" error occurred while performing the action.\n'
    'Please retry the operation after some time. If the error persists, '
    'contact the administrator for more information.'
)


def app_init_config(f):
    """Wrapper to allow an app initialized without config to behave like a normal app factory,
    and also allows you to instead create an app factory with given config.

    Example:
    ```python
    @app_init_config
    def init_app(config=None) -> FastAPI:
        ...

    # Normal
    uvicorn.run(init_app, factory=True)

    # With config, uvicorn part does not change
    app_with_config = init_app(config)
    uvicorn.run(app_with_config, factory=True)
    ```
    """

    @functools.wraps(f)
    def _init_app_wrapper(*args, **kwargs) -> FastAPI:
        if len(args) == 0 and len(kwargs) == 0:
            return f()
        return functools.partial(f, *args, **kwargs)

    return _init_app_wrapper


def init_logger(config_file: Optional[Path] = None):
    """Initialize logger using defaults, or from config file if given."""
    if config_file is None:
        logging.basicConfig(
            format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            level=logging.DEBUG,
        )

        # Only WARNING level for these packages
        logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    else:
        logging.config.fileConfig(config_file)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    This middleware will log all unhandled exceptions.
    Unhandled exceptions are all exceptions that are not HTTPExceptions or RequestValidationErrors.
    """
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    LOG.error(
        f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}>: {exception_value}',
        exc_info=exc,
    )

    return await http_exception_handler(
        request,
        HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=EXCEPTION_MESSAGE_FORMAT.format(exception_name=exception_name),
        ),
    )
