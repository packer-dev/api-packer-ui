from pydantic import BaseModel
from typing import Any, List

class DataType(BaseModel):
    type: str
    detail: List[Any]

class Prop(BaseModel):
    id: Any
    value: str
    dataType: DataType
    optional: bool
