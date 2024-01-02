from datetime import datetime, timedelta
from typing import List, Optional, Union
from uuid import uuid4
from .models import TaskState, WorkTask, WorkTaskIDType
from ...db import memdb

from reporttask.celery_app import app
from celery.canvas import Signature
from celery.result import AsyncResult


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
    def __init__(self, db):
        self.db = db

    async def get_task_from_id(self, task_id: WorkTaskIDType) -> Optional[WorkTask]:
        for i in self.db["tasks"]:
            if isinstance(i, WorkTask) and i.id == task_id:
                return i

    async def get_all_tasks(self) -> List[WorkTask]:
        return self.db["tasks"]

    async def save_work_task(self, task: WorkTask):
        print("Saving task", task)
        return

    async def create_and_save_task(
        self,
        task_name_or_signature: Union[str, Signature],
        work_task_name: Optional[str] = None,
        *args,
        **kwargs
    ) -> Optional[WorkTask]:
        task: Signature
        if isinstance(task_name_or_signature, Signature):
            # Signature passed
            task = task_name_or_signature
        elif isinstance(task_name_or_signature, str):
            # Task name passed, get signature
            task = app.signature(task_name_or_signature)
        else:
            raise TypeError("Invalid type of task name given.")

        task_result: AsyncResult = task.delay(*args, **kwargs)

        work_task = WorkTask(
            id=task_result.id,
            name=work_task_name or f"task_{task_result.id}",
            status=task_result.state,
            created_by_user=uuid4(),
            created_ts=datetime.utcnow(),
        )

        await self.save_work_task(work_task)

        return work_task
