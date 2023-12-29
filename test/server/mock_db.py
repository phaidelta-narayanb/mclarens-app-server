from datetime import datetime
from uuid import UUID

MOCK_DB = {
    'report': [
        dict(
            id=1,
            case_name="Canada House Fire",
            prompt="House fire",
            content=open("templates/final_report_test.html").read(),
            created_ts=datetime.fromtimestamp(1703831886.0),
            created_by=UUID("b7aea7d9-2fe3-4e27-82d5-ed681170ac5e"),
        )
    ]
}
