from pydantic import BaseModel
from typing import List, Any

class Code(BaseModel):
    expand: str
    collapse: str

class Show(BaseModel):
    code: Code
    name: str

class ListItem(BaseModel):
    id: Any
    text: str 
    index: int

class Content(BaseModel):
    id: Any
    text: str
    list: List[ListItem]
    type: str
    code: Show
    index: int