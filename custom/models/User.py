from pydantic import BaseModel
from typing import Any

class User(BaseModel):
    id: Any
    name: str
    status: bool
    age: int
    email: int
    timeCreated: str
    lastModifiedTime: str