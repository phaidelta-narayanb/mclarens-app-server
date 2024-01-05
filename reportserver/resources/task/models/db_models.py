from sqlalchemy import Column, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped

from datetime import datetime
import uuid as uuid_pkg

from reportserver.db import Base
from .data_models import WorkTaskInsert


class DBWorkTask(Base):
    __tablename__ = "work_task"

    uuid: Mapped[uuid_pkg.UUID] = Column("uuid", Uuid, primary_key=True)
    name: Mapped[str] = Column("task_name", String, nullable=True)
    created_by: Mapped[uuid_pkg.UUID] = Column("created_by", Uuid)  # TODO: FK
    created_ts: Mapped[datetime] = Column(
        "created_ts", DateTime(timezone=True), server_default=func.now()
    )
    updated_ts: Mapped[datetime] = Column(
        "updated_ts", DateTime(timezone=True), onupdate=func.now()
    )

    __table_args__ = (
        # Add constraints here
    )

    @classmethod
    def from_model(cls, model: WorkTaskInsert):
        return cls(
            uuid=model.id,
            name=model.name,
            created_by=model.created_by_user,
        )
