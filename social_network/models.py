from pydantic import BaseModel
from typing import Any, List, Optional
from fastapi import UploadFile, File
from datetime import datetime


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
    last_time_active: datetime
    time_created: datetime


class Member(BaseModel):
    id: str
    nickname: str
    user: User
    is_owner: bool


class ContentMessage(BaseModel):
    id: str
    text: str
    type: int  # 1. Normal # 2.Sticker # 3.Image/Video


class Message(BaseModel):
    id: str
    content: ContentMessage
    user: User
    time_created: datetime


class DataGroup(BaseModel):
    color: str
    emoji: str


class Group(BaseModel):
    id: str
    name: str
    members: List[Member]
    last_message: Message
    data: DataGroup
    time_created: datetime
    last_time_update: datetime
    image: str


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
    type: int  # 1. normal # 2.background


class Media(BaseModel):
    id: str
    url: str
    status: int
    type: int  # 1. image #2. video,
    folder: str


class Post(BaseModel):
    id: str
    user: User
    content: ContentPost
    time_created: datetime
    last_time_update: datetime
    type: int
    tags: List[User]
    feel: str


class PostPayload(BaseModel):
    post: Post
    media_new: Optional[List[UploadFile]] = File(...)
    media_old: Optional[List[Media]] = None

    def __iter__(self):
        return iter((self.post, self.media_new, self.media_old))


class PostDTO(BaseModel):
    post: Post
    medias: List[Media]


class Feel(BaseModel):
    id: str
    user: User
    post: Post
    type: int


class Comment(BaseModel):
    id: str
    user: User
    content: str
    time_created: datetime
    last_time_update: datetime
    level: int
    parent: str


class CommentPayload(BaseModel):
    post_id: str
    comment: Comment
    media_new: UploadFile = File(...)
    media_old: Optional[List[Media]] = None


class FileDTO(BaseModel):
    file: UploadFile = File(...)
    folder: str
