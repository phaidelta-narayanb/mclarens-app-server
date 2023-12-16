
from datetime import datetime
from fastapi import FastAPI, APIRouter


async def get_task_status(task_id: str):
    return {
        "id": task_id,
        "status": "PENDING",
        "progress": 0.0,
        "created_ts": datetime.now(),
        "updated_ts": datetime.now()
    }


def init_app(app: FastAPI):
    task_routes = APIRouter(prefix="/task")

    task_routes.add_api_route("/status/{task_id}", get_task_status, methods={"GET"})

    app.include_router(task_routes)
