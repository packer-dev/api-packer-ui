from fastapi import APIRouter, Form, UploadFile, File
from social_network.services.PostServices import (
    get_post_by_id_user,
    create_post,
    edit_post,
    delete_post,
)
from social_network.models import PostPayload, Post, Media
from typing import List, Optional
import json

router = APIRouter()


@router.get("/api/social-network/v1/post")
async def get_post_by_id_user_api(user_id: str, is_profile: str):
    return await get_post_by_id_user(user_id, is_profile)


@router.post("/api/social-network/v1/post")
async def create_post_api(
    post: str = Form(...),
    media_new: Optional[List[UploadFile]] = File(None),  # Set default to None
):
    post = json.loads(post)

    post = Post(
        id=post["id"],
        user=post["user"],
        content=post["content"],
        time_created=post["time_created"],
        last_time_update=post["last_time_update"],
        type=post["type"],
        tags=post["tags"],
        feel=post["feel"],
    )
    post_payload = PostPayload(media_new=media_new, post=post, media_old=[])
    return await create_post(post_payload)


@router.put("/api/social-network/v1/post")
async def edit_post_api(
    post: str = Form(...),
    media_new: Optional[List[UploadFile]] = File(None),  # Set default to None
    media_old: Optional[str] = Form(None),  # Set default to None
):
    post = json.loads(post)

    post = Post(
        id=post["id"],
        user=post["user"],
        content=post["content"],
        time_created=post["time_created"],
        last_time_update=post["last_time_update"],
        type=post["type"],
        tags=post["tags"],
        feel=post["feel"],
    )

    media_olds = json.loads(media_old)

    media_olds = [
        Media(
            id=media_old["id"],
            url=media_old["url"],
            status=media_old["status"],
            type=media_old["type"],
            folder=media_old["folder"],
        )
        for media_old in media_olds
    ]

    post_payload = PostPayload(media_new=media_new, post=post, media_old=media_olds)
    return await edit_post(post_payload)


@router.delete("/api/social-network/v1/post")
async def delete_post_api(post_id: str):
    return await delete_post(post_id)
