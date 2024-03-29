
from fastapi import FastAPI, APIRouter
from starlette.status import HTTP_201_CREATED

from . import views


def init_app(app: FastAPI):
    report_routes = APIRouter(prefix="/report", tags=["report-generator"])
    reports_routes = APIRouter(prefix="/reports", tags=["report-generator"])

    app.add_api_route("/report_export_formats", views.get_possible_export_formats, methods={"GET"})

    report_routes.add_api_route("", views.make_report, methods={"POST"}, status_code=HTTP_201_CREATED, tags=["task"])
    report_routes.add_api_route("/{report_id}", views.get_report, methods={"GET"})
    report_routes.add_api_route("/{report_id}/pdf", views.get_report_pdf, methods={"GET"})

    reports_routes.add_api_route("", views.get_report_list, methods={"GET"})
    reports_routes.add_api_route("/exportAll", views.get_reports_as_zip_export, methods={"GET"})

    app.include_router(report_routes)
    app.include_router(reports_routes)
