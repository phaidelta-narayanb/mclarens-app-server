from fastapi.params import Form
from pydantic import BaseModel


class CreatedWorkTask(BaseModel):
    task_id: str

