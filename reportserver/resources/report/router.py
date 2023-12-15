
from fastapi import FastAPI, APIRouter

from . import views


def init_app(app: FastAPI):
    report_routes = APIRouter(prefix="/report")
    reports_routes = APIRouter(prefix="/reports")

    report_routes.add_api_route("", views.make_report, methods={"POST"})

    reports_routes.add_api_route("/", views.get_report_list, methods={"GET"})
    reports_routes.add_api_route("/{report_id}", views.get_report, methods={"GET"})
    reports_routes.add_api_route("/{report_id}/pdf", views.get_report_pdf, methods={"GET"})

    app.include_router(report_routes)
    app.include_router(reports_routes)
