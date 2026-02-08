from typing import List
from pydantic import BaseModel

class FieldValue(BaseModel):
    value: str
    confidence: float

class OrderPosition(BaseModel):
    article_number: FieldValue
    description: FieldValue
    kvk: FieldValue
    wgp: FieldValue

class ExtractionResult(BaseModel):
    positions: List[OrderPosition]
    total_pages: int
