import asyncio
from datetime import datetime, timedelta
import random
from typing import List
from uuid import uuid4
from fastapi import Request

from sse_starlette.sse import EventSourceResponse

from .models import Task

# TODO: CLI Arguments to enable different modes (eg: flag to show no tasks, flag to show 10 tasks, flag to show only done tasks, etc.)
# TODO: Same for other resources


async def get_task_status(task_id: str) -> Task:
    return Task(
        id=task_id,
        status="PENDING",
        progress=0.0,
        queue_position=999,
        estimated_queue_time=timedelta(days=2, minutes=30),
        created_by_user=uuid4(),
        created_ts=datetime.utcnow(),
        updated_ts=datetime.utcnow(),
    )


async def get_all_tasks_status() -> List[Task]:
    return [
        Task(
            id="699e7dd6d6524bc7a8b9610f8cfb40a8",
            status="PENDING",
            progress=0.0,
            queue_position=999,
            estimated_queue_time=timedelta(days=2, minutes=30),
            created_by_user=uuid4(),
            created_ts=datetime.now(),
            updated_ts=datetime.now(),
        )
    ]


async def dummy_task_status_generator(request: Request, task_id):
    c_time = datetime.utcnow()
    while True:
        yield Task(
            id=task_id,
            status="PENDING",
            progress=0.0,
            queue_position=999,
            estimated_queue_time=timedelta(days=2, minutes=30),
            created_by_user=uuid4(),
            created_ts=c_time,
            updated_ts=datetime.utcnow(),
        )
        await asyncio.sleep(random.uniform(0.1, 5.0))


async def live_task_status(request: Request, task_id: str) -> EventSourceResponse:
    return EventSourceResponse(dummy_task_status_generator(request, task_id))
