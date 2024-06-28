from pydantic import BaseModel
from typing import List


class Role(BaseModel):
    role: str
    content: str


class TextProps(BaseModel):
    id: float
    content: str
    type: str


class Message(BaseModel):
    id: float
    type: str
    content: List[TextProps]
    contentSearch: str
    rendered: bool


class MessageChild(BaseModel):
    id: float
    list: List[Message]
    isLoading: bool
    index: int


class History(BaseModel):
    id: float
    name: str
    messages: List[MessageChild]


class ChatGPT(BaseModel):
    list: List[History]
    userId: str
