from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import Form
from pydantic import BaseModel, ConfigDict


class CreateReportTask(BaseModel):
    inference_model_name: str
    incident_claim_type: str

    @classmethod
    async def as_form(
        cls, inference_model_name: str = Form(...), incident_claim_type: str = Form(...)
    ):
        return cls(
            inference_model_name=inference_model_name,
            incident_claim_type=incident_claim_type,
        )


class GeneratedReport(BaseModel):
    id: int
    case_name: str
    case_ref: Optional[str] = None
    prompt: Optional[str] = None

    created_ts: datetime
    created_by: UUID
    updated_ts: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GeneratedReportSource(GeneratedReport):
    content: str
