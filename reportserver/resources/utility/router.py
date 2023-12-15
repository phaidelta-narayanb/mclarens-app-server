
from fastapi import FastAPI, APIRouter

from . import views


def init_app(app: FastAPI):
    routes = APIRouter(prefix="/utility")

    routes.add_api_route("/html2pdf", views.make_pdf, methods={"POST"})

    app.include_router(routes)
