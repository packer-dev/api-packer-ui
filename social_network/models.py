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
    cover: str
    last_time_active: str


class Member(BaseModel):
    id: str
    nickname: str
    user: User
    is_owner: bool


class Message(BaseModel):
    id: str
    content: str
    user: User
    time: str


class Group(BaseModel):
    id: str
    name: str
    members: List[Member]
    last_message: Message
    data: Any
    time_created: str
    last_time_update: str


class SendMessageDTO(BaseModel):
    message: Message
    group: Group


class Relationship(BaseModel):
    id: str
    user1: str  # current
    user2: str  # visit
    status: int  # 1. send # 2. receive #3. friends #4. block


class ContentPost(BaseModel):
    id: str
    text: str
    data: Any
    type: int


class MediaPost(BaseModel):
    id: str
    url: str
    status: int
    type: int  # 1. image #2. video


class Post(BaseModel):
    id: str
    user: User
    content: ContentPost
    media: List[MediaPost]
    time_created: str
    last_time_update: str
    type: int
    tags: List[User]
    feel: str


class Feel(BaseModel):
    id: str
    user: User
    post: Post
    type: int


class Comment(BaseModel):
    id: str
    user: User
    content: str
    time_created: str
    last_time_update: str
    level: int
    parent: str
