from pydantic import BaseModel


class CreatedWorkTask(BaseModel):
    task_id: str
