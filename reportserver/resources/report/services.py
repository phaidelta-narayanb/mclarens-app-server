from datetime import datetime
from typing import Optional
from uuid import uuid4

from reportgen.report_export import ReportExporter

from reportserver.db import memdb
from ..task.models import WorkTask
from ..task.services import TaskService

from .models import GeneratedReport, GeneratedReportSource


memdb["reports"] = []

if len(memdb["reports"]) == 0:
    memdb["reports"].extend(
        [
            dict(
                id=1,
                case_name="Canada House Fire",
                prompt="House fire",
                content=open("templates/final_report_test.html").read(),
                created_ts=datetime.utcnow(),
                created_by=uuid4(),
            )
        ]
    )


class ReportService:
    def __init__(self, db):
        self.db = db

    async def get_generated_report_from_id(self, report_id: int):
        for i in self.db["reports"]:
            if i["id"] == report_id:
                return GeneratedReport.model_validate(i)

    async def get_generated_report_with_source_from_id(self, report_id: int):
        for i in self.db["reports"]:
            if i["id"] == report_id:
                return GeneratedReportSource.model_validate(i)

    async def get_generated_reports_with_source(self):
        return list(map(GeneratedReportSource.model_validate, self.db["reports"]))

    async def get_generated_reports(self):
        return list(map(GeneratedReport.model_validate, self.db["reports"]))

    # TODO: Cached file check by hash
    async def get_generated_report_pdf(
        self, report_id: int, report_exporter: ReportExporter
    ):
        report = await self.get_generated_report_with_source_from_id(report_id)
        return report_exporter.make_pdf(report.content)

    async def create_report_generate_task(
        self, inference_model_name, incident_claim_type, images, task_service: TaskService
    ) -> Optional[WorkTask]:
        return await task_service.create_and_save_task(
            "image_caption_to_report",
            work_task_name=incident_claim_type,
            model=inference_model_name,
            claim_type=incident_claim_type,
            attachment=dict(images=images)
        )
