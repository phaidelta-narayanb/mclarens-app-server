from typing import Optional
import unittest

from ..mock_db import MOCK_DB

from reportserver.resources.report.models import GeneratedReport
from reportserver.resources.report import services as report_services


class TestReportDB(unittest.TestCase):
    async def test_fetch_single_report(self):
        svc = report_services.ReportService(MOCK_DB)

        report: Optional[GeneratedReport] = await svc.get_generated_report_from_id(
            report_id=1
        )

        self.assertIsNotNone(report)
        self.assertEquals(report.creatcase_nameed_by, "Canada House Fire")
