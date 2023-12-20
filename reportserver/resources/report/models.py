from typing import List, Optional
from fastapi import Form
from pydantic import BaseModel, AnyUrl


class CreateReportTask(BaseModel):
    inference_model_name: str
    incident_claim_type: str

    @classmethod
    async def as_form(
        cls,
        inference_model_name: str = Form(...),
        incident_claim_type: str = Form(...)
    ):
        return cls(inference_model_name=inference_model_name, incident_claim_type=incident_claim_type)


class GeneratedReport(BaseModel):
    id: int
    case_name: str
    case_ref: Optional[str] = None
    prompt: Optional[str] = None


class GeneratedReportSource(GeneratedReport):
    content: str
