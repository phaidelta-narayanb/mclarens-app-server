
from sqlalchemy import select
from sqlalchemy.engine.result import ScalarResult

from .session import Session


class ReadableMixin:
    """Mixin class for tables to add methods to fetch all records in the table."""
    @classmethod
    async def read_all(cls, session: Session) -> ScalarResult:
        return await session.scalars(select(cls))
