import tempfile
from typing import List
import zipfile
from fastapi import Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from starlette.status import HTTP_404_NOT_FOUND
from reportserver.resources.report.services import ReportService

# Cross-dependency on `tasks` resource
from reportserver.resources.task.models import WorkTask
from reportserver.resources.task.services import TaskService
from reportserver.resources.task.views import get_task_service

from .models import CreateReportTask, GeneratedReport, GeneratedReportSource


async def get_report_service() -> ReportService:
    # TODO: Use proper db session maker
    from reportserver.db import memdb
    return ReportService(memdb)


async def get_possible_export_formats() -> List[str]:
    return [".pdf"]


async def make_report(
    request: Request,
    inference_params: CreateReportTask = Depends(CreateReportTask.as_form),
    images: List[UploadFile] = File(None),
    report_service: ReportService = Depends(get_report_service),
    task_service: TaskService = Depends(get_task_service)
) -> WorkTask:
    """Create a task to generate a report from the given prompt and images."""

    # TODO: Complete OpenAI and Celery stuff
    # TODO: How to return live progress (%)? Decide between SSE, REST and WS
    return await report_service.create_report_generate_task(
        inference_params.inference_model_name,
        inference_params.incident_claim_type,
        images,
        task_service
    )


async def get_report_list(
    request: Request, report_service: ReportService = Depends(get_report_service)
) -> List[GeneratedReport]:
    """Get list of all created reports."""
    return await report_service.get_generated_reports()


async def get_report(
    request: Request,
    report_id: int,
    report_service: ReportService = Depends(get_report_service),
) -> GeneratedReportSource:
    """Get report with given id."""
    report = await report_service.get_generated_report_with_source_from_id(report_id)
    if report is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"Requested report with ID '{report_id}' not found.",
        )

    return report


async def get_report_pdf(
    request: Request,
    report_id: int,
    report_service: ReportService = Depends(get_report_service),
) -> FileResponse:
    """Get report PDF with given id."""
    pdf_response = await report_service.get_generated_report_pdf(
        report_id, request.app.extra["report_exporter"]
    )

    if pdf_response is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"Requested report with ID '{report_id}' not found.",
        )

    return FileResponse(pdf_response)


async def get_reports_as_zip_export(format: str = ".pdf") -> FileResponse:
    zip_export_file = tempfile.mktemp(".zip")
    with zipfile.ZipFile(zip_export_file, mode="w") as zf:
        zf.comment = "Test".encode()
    return FileResponse(zip_export_file)
