from pydantic import BaseModel
from typing import Optional


class QAndA(BaseModel):
    question: str
    answer: str
