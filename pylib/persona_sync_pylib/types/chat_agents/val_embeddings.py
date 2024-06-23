from pydantic import BaseModel
from typing import List


class ValEmbeddings(BaseModel):
    value: str
    embeddings: List[float]
    tracking_id: str
