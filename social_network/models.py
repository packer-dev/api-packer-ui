from pydantic import BaseModel
from typing import Any, List, Optional
from fastapi import UploadFile, File
from typing import Any


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
    time_created: str
    bio: str


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
    time_created: str


class DataGroup(BaseModel):
    color: str
    emoji: str


class Group(BaseModel):
    id: str
    name: str
    members: List[Member]
    last_message: Message
    data: DataGroup
    time_created: str
    last_time_update: str
    image: str
    seen: Any
    multiple: bool


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
    time_created: str
    last_time_update: str
    type: int
    tags: List[User]
    feel: str
    background: str
    answer_question: str
    local: str


class PostPayload(BaseModel):
    post: Post
    media_new: Optional[List[UploadFile]] = None
    media_old: List[Media] = []

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


class ContentComment(BaseModel):
    id: str
    text: str
    type: int  # 1. Normal # 2.Sticker # 3.Image/Video


class Comment(BaseModel):
    id: str
    user: User
    content: ContentComment
    time_created: str
    last_time_update: str
    level: int
    parent: str


class CommentPayload(BaseModel):
    post_id: str
    comment: Comment
    media_new: Optional[List[UploadFile]] = File(...)
    media_old: Optional[List[Media]] = None


class FileDTO(BaseModel):
    file: UploadFile = File(...)
    folder: str


class RelationshipPayload(BaseModel):
    user1: str
    user2: str
    status: str


class Notification(BaseModel):
    id: str
    type: int  # 1 love #2 comment #3 reply comment
    main_id: str
    user: User
    time_created: str
    is_read: bool
    last_time_update: str
