from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Task(BaseModel):
    id: str
    name: str
    status: str
    progress: Optional[float] = None
    queue_position: Optional[int] = None
    estimated_queue_time: Optional[timedelta] = None
    created_by_user: UUID
    created_ts: datetime
    updated_ts: datetime
