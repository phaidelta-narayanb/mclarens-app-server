import asyncio
import logging
from typing import List, Optional, Union
from uuid import uuid4

from celery.canvas import Signature
from celery.result import AsyncResult

# SQL operations
from sqlalchemy import sql

from reportserver.db import Session
from reporttask.celery_app import app

from .models import DBWorkTask, WorkTask, WorkTaskIDType, WorkTaskInsert

LOG = logging.getLogger()


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    async def _generate_work_task_from_db_model(
        self, work_task: Optional[DBWorkTask]
    ) -> WorkTask:
        # Early return (None) if the given task entry is not found
        if work_task is None:
            return

        task_result = AsyncResult(str(work_task.uuid), app=app)
        task_error = (
            task_result.backend.prepare_exception(task_result.result)
            if task_result.failed()
            else None
        )

        return WorkTask(
            id=work_task.uuid,
            name=work_task.name,
            status=task_result.state,
            error=task_error,
            has_result=task_result.ready(),
            created_by_user=work_task.created_by,
            created_ts=work_task.created_ts,
            updated_ts=work_task.updated_ts,
        )

    async def get_task_from_id(self, task_id: WorkTaskIDType) -> Optional[WorkTask]:
        LOG.info("Fetching task with uuid '%s'", task_id)
        async with self.db as sess:
            result = await sess.execute(sql.select(DBWorkTask).filter_by(uuid=task_id))
            return await self._generate_work_task_from_db_model(result.scalar())

    async def get_all_tasks(self) -> List[WorkTask]:
        LOG.info("Fetching tasks list")
        async with self.db as sess:
            result = await sess.execute(sql.select(DBWorkTask))
            return await asyncio.gather(
                *map(self._generate_work_task_from_db_model, result.scalars())
            )

    async def save_work_task(self, task: WorkTaskInsert) -> WorkTask:
        LOG.info("Saving new task with uuid '%s'", task.id)
        async with self.db as sess:
            # Save work task into db
            sess.add(DBWorkTask.from_model(task))
            await sess.commit()
            # Fetch and return the result
            result = await sess.execute(sql.select(DBWorkTask).filter_by(uuid=task.id))
            newly_inserted_task = await self._generate_work_task_from_db_model(
                result.scalar()
            )
            if newly_inserted_task is None:
                raise RuntimeError(
                    "Failed to verify that task '%s' was inserted into the database."
                    % task.id
                )
            return newly_inserted_task

    async def create_and_save_task(
        self,
        task_name_or_signature: Union[str, Signature],
        work_task_name: Optional[str] = None,
        *args,
        **kwargs,
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

        work_task = WorkTaskInsert(
            id=task_result.id,
            name=work_task_name or f"task_{task_result.id}",
            status=task_result.state,
            created_by_user=uuid4(),
        )

        return await self.save_work_task(work_task)
