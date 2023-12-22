import asyncio
from typing import List
from fastapi import Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from starlette.status import HTTP_404_NOT_FOUND
from reportserver.resources.report.services import ReportService

from reportserver.resources.task.models import WorkTask

from .models import CreateReportTask, GeneratedReport, GeneratedReportSource


async def make_report(
    request: Request,
    inference_params: CreateReportTask = Depends(CreateReportTask.as_form),
    images: List[UploadFile] = File(None),
    report_service: ReportService = Depends(ReportService),
) -> WorkTask:
    """Create a task to generate a report from the given prompt and images."""

    print("=== Extracted information ===")
    print("Model name:", inference_params.inference_model_name)
    print("Incident claim type:", inference_params.incident_claim_type)
    print()
    print("Images:", images)

    print()
    print("Waiting for some time to simulate celery inserting...")
    await asyncio.sleep(2.0)

    # TODO: Complete OpenAI and Celery stuff
    # TODO: How to return live progress (%)? Decide between SSE, REST and WS
    return await report_service.create_report_generate_task(
        inference_params.inference_model_name,
        inference_params.incident_claim_type,
        images,
    )


async def get_report_list(
    request: Request, report_service: ReportService = Depends(ReportService)
) -> List[GeneratedReport]:
    """Get list of all created reports."""
    return await report_service.get_generated_reports()


async def get_report(
    request: Request,
    report_id: int,
    report_service: ReportService = Depends(ReportService),
) -> GeneratedReportSource:
    """Get report with given id."""
    report = await report_service.get_generated_report_with_source_from_id(report_id)
    if report is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail=f"Requested report with ID '{report_id}' not found.",
        )

    return report

    # FIXME: Dummy response
    return GeneratedReportSource(
        id=report_id,
        case_name="Canada House Fire",
        prompt="House fire",
        content=await request.app.extra["report_maker"].from_template_async(
            "deafult_mclarens_report_template.j2.html"
        ),
    )


async def get_report_pdf(
    request: Request,
    report_id: int,
    report_service: ReportService = Depends(ReportService),
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
