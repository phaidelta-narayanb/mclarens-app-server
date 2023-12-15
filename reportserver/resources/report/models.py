
from typing import Optional
from pydantic import BaseModel


class GeneratedReport(BaseModel):
    id: int
    prompt: Optional[str]



class GeneratedReportSource(GeneratedReport):
    content: str

