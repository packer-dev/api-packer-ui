from pydantic import BaseModel
from typing import Any, List


class LoginDTO(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    avatar: str
    lastTimeActive: str


class Member(BaseModel):
    id: str
    nickname: str
    user: User


class Message(BaseModel):
    id: str
    content: str
    type: str
    user: User
    time: str


class Group(BaseModel):
    id: str
    name: str
    members: List[Member]
    messages: List[Message]
    data: Any
    timeCreated: str
    lastTimeUpdate: str


class SendMessageDTO(BaseModel):
    message: Message
    group: Group
