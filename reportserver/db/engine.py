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


Session = AsyncSession
Transaction = AsyncTransaction
Connection = AsyncConnection


@lru_cache()
def get_engine(db_settings: DBSettings = DBSettings()) -> AsyncEngine:
    """Create and return a db engine using the config"""
    schema_mapping = get_schema_mapping()

    return create_async_engine(
        db_settings.db_uri,
        pool_pre_ping=True,
        execution_options={"schema_translate_map": schema_mapping},
    )


@lru_cache()
def get_sessionmaker():
    """Return a sessionmaker object that uses the above engine"""
    engine = get_engine()
    return sessionmaker(bind=engine, class_=Session, autoflush=False, future=True)


@lru_cache()
def get_schema_mapping(db_settings: DBSettings = DBSettings()) -> Dict[str, str]:
    if db_settings.db_schema_map:
        return dict(mapping.split(":") for mapping in db_settings.db_schema_map)
    return {}
