from pydantic import BaseModel
from typing import Any

class Category(BaseModel):
    id: Any
    name: str
    timeCreated: str
    lastModifiedTime: str