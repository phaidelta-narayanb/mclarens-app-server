from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError

from .config import DBSettings
from .engine import Session, get_sessionmaker

LOG = logging.getLogger(__name__)


@asynccontextmanager
async def get_session(db_settings: DBSettings) -> AsyncIterator[Session]:
    """Returns sessionmaker when it is available"""
    db: Session
    sessionmaker = get_sessionmaker(db_settings)

    try:
        async with sessionmaker() as db:
            LOG.debug("Creating DB session")
            yield db
    except SQLAlchemyError:
        LOG.exception("Failed to create SQLaAlchemy session.")
    finally:
        LOG.debug("Closing DB session")
        sessionmaker.close_all()
