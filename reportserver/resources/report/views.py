import asyncio
from typing import List
from uuid import uuid4
from fastapi import Depends, File, HTTPException, Request, Response, UploadFile
from fastapi.responses import FileResponse

from starlette.status import HTTP_404_NOT_FOUND

from reportserver.models import CreatedWorkTask

from .models import CreateReportTask, GeneratedReport, GeneratedReportSource


async def make_report(
    request: Request,
    inference_params: CreateReportTask = Depends(CreateReportTask.as_form),
    images: List[UploadFile] = File(None),
) -> CreatedWorkTask:
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
    return CreatedWorkTask(task_id=uuid4().hex)


async def get_report_list(request: Request) -> List[GeneratedReport]:
    """Get list of all created reports."""
    return [GeneratedReport(id=1, case_name="Canada House Fire", prompt="House fire")]


async def get_report(request: Request, report_id: int) -> GeneratedReportSource:
    """Get report with given id."""
    if report_id != 1:
        raise HTTPException(HTTP_404_NOT_FOUND, detail=f"Requested report with ID '{report_id}' not found.")

    # FIXME: Dummy response
    return GeneratedReportSource(
        id=report_id,
        case_name="Canada House Fire",
        prompt="House fire",
        content=await request.app.extra["report_maker"].from_template_async(
            "deafult_mclarens_report_template.j2.html"
        ),
    )


async def get_report_pdf(request: Request, report_id: int) -> FileResponse:
    """Get report PDF with given id."""
    if report_id != 1:
        raise HTTPException(HTTP_404_NOT_FOUND, detail=f"Requested report with ID '{report_id}' not found.")

    # TODO: Fetch pre-generated file based on ID instead of re-generating it every time
    return FileResponse(
        request.app.extra["report_exporter"].make_pdf(
            await request.app.extra["report_maker"].from_template_async(
                "deafult_mclarens_report_template.j2.html"
            )
        )
    )
