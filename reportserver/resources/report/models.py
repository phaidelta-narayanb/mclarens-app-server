from typing import List, Optional
from pydantic import BaseModel, AnyUrl


class CreateReportTask(BaseModel):
    model_name: str
    prompt: Optional[str]
    images: List[AnyUrl]


class GeneratedReport(BaseModel):
    id: int
    prompt: Optional[str]


class GeneratedReportSource(GeneratedReport):
    content: str
