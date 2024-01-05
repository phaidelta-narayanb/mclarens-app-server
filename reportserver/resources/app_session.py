from typing import AsyncIterator
from fastapi import Request

from reportserver.db import Session, get_session


ERROR_MSG_NO_DB_CONFIG = (
    "FastAPI Application's `extra` config parameter 'db_settings' is missing.\n"
    "Please specify it in the `FastAPI` constructor."
)
"""Message shown if `db_settings` is not set in the app."""


async def get_app_db_session(request: Request) -> AsyncIterator[Session]:
    """Gets a new Database Session object using the config from the application."""
    try:
        async with get_session(request.app.extra["db_settings"]) as session:
            yield session
    except KeyError as e:
        raise KeyError(ERROR_MSG_NO_DB_CONFIG) from e
