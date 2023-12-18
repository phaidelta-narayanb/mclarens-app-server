from fastapi import FastAPI, APIRouter

from .views import get_all_tasks_status, get_task_status, live_task_status


def init_app(app: FastAPI):
    task_routes = APIRouter(prefix="/task", tags=["task"])
    tasks_routes = APIRouter(prefix="/tasks", tags=["task"])

    task_routes.add_api_route("/status/{task_id}", get_task_status, methods={"GET"})
    task_routes.add_api_route("/status/{task_id}/live", live_task_status, methods={"GET"})

    tasks_routes.add_api_route("/status", get_all_tasks_status, methods={"GET"})

    app.include_router(task_routes)
    app.include_router(tasks_routes)
