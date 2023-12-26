from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4
from .models import TaskState, WorkTask, WorkTaskIDType
from ...db import memdb

memdb["tasks"] = []

if len(memdb["tasks"]) == 0:
    memdb["tasks"].extend(
        [
            WorkTask(
                id="aaaabbbbccccdddd",
                name="Dummy task",
                status=TaskState.STARTED,
                progress=0.50,
                created_by_user=uuid4(),
                created_ts=datetime.utcnow(),
            ),
            WorkTask(
                id="eeeeffffgggghhhh",
                name="Dummy task 2",
                queue_position=2,
                created_by_user=uuid4(),
                created_ts=datetime.utcnow(),
            ),
            WorkTask(
                id="iiiijjjjkkkkllll",
                name="Dummy task 3",
                status=TaskState.PENDING,
                queue_position=5,
                estimated_queue_time=timedelta(minutes=59),
                created_by_user=uuid4(),
                created_ts=datetime.utcnow(),
            ),
        ]
    )


class TaskService:
    def __init__(self):
        global memdb
        self.db = memdb

    async def get_task_from_id(self, task_id: WorkTaskIDType) -> Optional[WorkTask]:
        for i in self.db["tasks"]:
            if isinstance(i, WorkTask) and i.id == task_id:
                return i

    async def get_all_tasks(self) -> List[WorkTask]:
        return self.db["tasks"]
