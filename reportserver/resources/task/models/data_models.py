from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from enum import Enum

from reportserver.resources.models import ExceptionSchema

WorkTaskIDType = UUID


class TaskState(str, Enum):
    PENDING = "PENDING"
    """Task state is unknown (assumed pending since you know the id)."""
    RECEIVED = "RECEIVED"
    """Task was received by a worker (only used in events)."""
    STARTED = "STARTED"
    """Task was started by a worker (:setting:`task_track_started`)."""
    SUCCESS = "SUCCESS"
    """Task succeeded"""
    FAILURE = "FAILURE"
    """Task failed"""
    REVOKED = "REVOKED"
    """Task was revoked."""
    REJECTED = "REJECTED"
    """Task was rejected (only used in events)."""
    RETRY = "RETRY"
    """Task is waiting for retry."""
    IGNORED = "IGNORED"


class WorkTaskInsert(BaseModel):
    id: WorkTaskIDType
    name: str
    status: TaskState = TaskState.PENDING
    error: Optional[ExceptionSchema] = None
    created_by_user: UUID


class WorkTask(BaseModel):
    id: WorkTaskIDType
    name: str
    status: TaskState = TaskState.PENDING
    error: Optional[ExceptionSchema] = None
    has_result: bool = False
    progress: Optional[float] = None
    queue_position: Optional[int] = None
    estimated_queue_time: Optional[timedelta] = None
    created_by_user: UUID
    created_ts: datetime
    updated_ts: Optional[datetime] = None
