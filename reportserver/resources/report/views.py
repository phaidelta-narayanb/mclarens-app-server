from typing import List
from uuid import uuid4
from fastapi import Request, Response
from fastapi.responses import FileResponse

from reportserver.models import CreatedWorkTask

from .models import CreateReportTask, GeneratedReport, GeneratedReportSource


async def make_report(request: Request, params: CreateReportTask) -> CreatedWorkTask:
    """Create a task to generate a report from the given prompt and images."""
    # TODO: Complete OpenAI and Celery stuff
    # TODO: How to return live progress (%)?
    return CreatedWorkTask(
        task_id=uuid4().hex
    )


async def get_report_list(request: Request) -> List[GeneratedReport]:
    """Get list of all created reports."""
    return [GeneratedReport(id=1, prompt="")]


async def get_report(request: Request, report_id: int) -> GeneratedReportSource:
    """Get report with given id."""
    return GeneratedReportSource(
        id=report_id,
        prompt="",
        content=await request.app.extra["report_maker"].from_template_async(
            "deafult_mclarens_report_template.j2.html"
        ),
    )


async def get_report_pdf(request: Request, report_id: int) -> FileResponse:
    """Get report PDF with given id."""
    # TODO: Fetch pre-generated file based on ID instead of re-generating it every time
    return FileResponse(
        request.app.extra["report_exporter"].make_pdf(
            await request.app.extra["report_maker"].from_template_async(
                "deafult_mclarens_report_template.j2.html"
            )
        )
    )
