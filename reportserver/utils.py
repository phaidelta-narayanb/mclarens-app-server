
import logging
import logging.config
import functools
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI


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
    def _init_app_wrapper(config: Optional[Any] = None) -> FastAPI:
        if config is None:
            return f()
        return functools.partial(f, config=config)

    return _init_app_wrapper


def init_logger(config_file: Optional[Path] = None):
    """Initialize logger using defaults, or from config file if given."""
    if config_file is None:
        logging.basicConfig(
            format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            level=logging.DEBUG,
        )

        # Debug only WARNING level for these packages
        logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    else:
        logging.config.fileConfig(config_file)
