from fastapi import APIRouter, UploadFile, File, Form
from social_network.services.CommentServices import (
    get_comment_by_id_post,
    send_comment,
    delete_comment,
)
from social_network.models import CommentPayload, Comment
from typing import Optional, List
import json

router = APIRouter(prefix="/api/social-network/v1/comment")


@router.get("/id")
async def get_comment_by_id_post_api(post_id: str, limit: int = 10, offset: int = 0):
    return await get_comment_by_id_post(post_id=post_id, limit=limit, offset=offset)


@router.post("")
async def sent_comment_api(
    post_id: str = Form(...),
    comment: str = Form(...),
    media_new: Optional[List[UploadFile]] = File(None),  # Set default to None
    media_old: Optional[str] = Form(None),  # Set default to None):
):
    comment = json.loads(comment)
    comment = Comment(
        id=comment["id"],
        user=comment["user"],
        content=comment["content"],
        time_created=comment["time_created"],
        last_time_update=comment["last_time_update"],
        level=comment["level"],
        parent=comment["parent"],
    )
    comment_payload = CommentPayload(
        post_id=post_id, comment=comment, media_new=media_new, media_old=media_old
    )
    return await send_comment(comment_payload)


@router.delete("")
async def sent_comment_api(comment_id: str, post_id: str):
    return await delete_comment(post_id, comment_id)
