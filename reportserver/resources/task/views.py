from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

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
