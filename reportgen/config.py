from pydantic import BaseModel

from typing import List, Dict, Literal, Union, Optional


class UploadSettings(BaseModel):
    allowed_types: Optional[List[str]] = None


class ClientSettings(BaseModel):
    system_prompt: str
    user_prompts: List[Union[str, Dict[str, str]]]


class ReportSettings(BaseModel):
    templates_dir: str = "templates/"
    report_template_file: str
    export_method: Literal["pandoc", "weasyprint"] = "pandoc"

    logo_image_url: Optional[str] = None


class CustomerSettings(BaseModel):
    report: ReportSettings


class GenerationSettings(BaseModel):
    upload: UploadSettings
    client: ClientSettings
    customer: CustomerSettings
