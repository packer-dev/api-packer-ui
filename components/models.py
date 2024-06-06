from pydantic import BaseModel
from typing import Any, Optional, List

class Component(BaseModel):
    id: Any
    name: str
    type: str
    contents: Optional[List[Any]]
    props: Optional[List[Any]]


