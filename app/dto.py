from typing import Optional, List
from pydantic import BaseModel

class FieldValue(BaseModel):
    value: str
    confidence: float

class OrderPosition(BaseModel):
    article_number: FieldValue
    description: FieldValue
    kvk: FieldValue
    wgp: FieldValue
    quantity: FieldValue
    price: FieldValue
    total: FieldValue
    page_number: Optional[int] = None
    row_index: Optional[int] = None

class ExtractionResult(BaseModel):
    positions: List[OrderPosition]
    total_pages: int
