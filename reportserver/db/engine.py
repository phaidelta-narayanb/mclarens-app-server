from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncTransaction,
    AsyncConnection,
    AsyncEngine,
)

from sqlalchemy.orm import sessionmaker

from .config import DBSettings

from functools import lru_cache

from typing import Dict

# Type definitions

Engine = AsyncEngine
Session = AsyncSession
Connection = AsyncConnection
Transaction = AsyncTransaction


@lru_cache()
def get_engine(db_settings: DBSettings) -> Engine:
    """Create and return a db engine using the config"""
    # schema_mapping = get_schema_mapping()

    return create_async_engine(
        url=str(db_settings.db_uri),
        pool_pre_ping=True,
        # execution_options={"schema_translate_map": schema_mapping},
    )


@lru_cache()
def get_sessionmaker(db_settings: DBSettings) -> sessionmaker[Session]:
    """Return a sessionmaker object that uses the above engine"""
    return sessionmaker(
        bind=get_engine(db_settings),
        class_=Session,
        autoflush=False,
        future=True,
    )


@lru_cache()
def get_schema_mapping(db_settings: DBSettings) -> Dict[str, str]:
    if db_settings.db_schema_map:
        return dict(mapping.split(":") for mapping in db_settings.db_schema_map)
    return {}
