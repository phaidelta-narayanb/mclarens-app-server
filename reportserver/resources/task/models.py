from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel


class Task(BaseModel):
    id: str
    status: str
    progress: float
    queue_position: int
    estimated_queue_time: timedelta
    created_by_user: UUID
    created_ts: datetime
    updated_ts: datetime
