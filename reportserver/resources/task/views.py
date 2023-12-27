import asyncio
from datetime import datetime
import random
from typing import List
from fastapi import HTTPException, Request, Depends
from starlette.status import HTTP_404_NOT_FOUND

from sse_starlette.sse import EventSourceResponse

from .services import TaskService

from .models import WorkTask, TaskState, WorkTaskIDType

# TODO: CLI Arguments to enable different modes (eg: flag to show no tasks, flag to
# show 10 tasks, flag to show only done tasks, etc.)
# TODO: Same for other resources


async def get_task_service() -> TaskService:
    # TODO: Use proper db session maker
    from reportserver.db import memdb
    return TaskService(memdb)


async def get_task_status(
    task_id: WorkTaskIDType, task_service: TaskService = Depends(get_task_service)
) -> WorkTask:
    task = await task_service.get_task_from_id(task_id)
    if task is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"Requested task with ID '{task_id}' not found.",
        )
    return task


async def get_all_tasks_status(
    task_service: TaskService = Depends(get_task_service),
) -> List[WorkTask]:
    return await task_service.get_all_tasks()


async def dummy_task_status_generator(
    request: Request, task_id: WorkTaskIDType, task_service: TaskService
):
    while True:
        yield await task_service.get_task_from_id(task_id)
        await asyncio.sleep(random.uniform(0.1, 5.0))


async def dummy_tasks_status_generator(request: Request, task_service: TaskService):
    while True:
        if await request.is_disconnected():
            break

        tasks = await task_service.get_all_tasks()
        for t in tasks:
            t.updated_ts = datetime.utcnow()
            if t.status == TaskState.STARTED:
                if t.progress is None:
                    t.progress = 0.0
                t.progress -= (t.progress - 1.0) * 0.9
        yield tasks
        await asyncio.sleep(random.uniform(0.1, 5.0))


async def live_task_status(
    request: Request, task_id: str, task_service: TaskService = Depends(get_task_service)
) -> EventSourceResponse:
    return EventSourceResponse(
        dummy_task_status_generator(request, task_id, task_service)
    )


async def live_all_task_status(
    request: Request, task_service: TaskService = Depends(get_task_service)
) -> EventSourceResponse:
    return EventSourceResponse(dummy_tasks_status_generator(request, task_service))
