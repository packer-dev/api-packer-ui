from pydantic import BaseModel
from typing import List


class Role(BaseModel):
    role: str
    content: str


class TextProps(BaseModel):
    id: str
    content: str
    type: str


class Message(BaseModel):
    id: str
    type: str
    content: List[TextProps]
    contentSearch: str
    rendered: bool


class MessageChild(BaseModel):
    id: str
    list: List[Message]
    isLoading: bool
    index: int


class History(BaseModel):
    id: str
    name: str
    messages: List[MessageChild]
    timeSaved: str = None
    isArchive: bool


class ChatGPT(BaseModel):
    history: History
    userId: str
