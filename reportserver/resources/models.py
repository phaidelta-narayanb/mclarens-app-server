

from typing import List
from pydantic import BaseModel


class ExceptionSchema(BaseModel):
    exc_type: str
    exc_message: List[str]
    exc_module: str
