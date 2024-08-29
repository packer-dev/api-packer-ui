from firebase_admin import db
from social_network.models import CommentPayload
from utils import new_value, upload_media_db
import uuid


async def get_comment_by_id_post(post_id: str, limit: int = 10, offset: int = 0):
    ref = db.reference("social-network")
    comments = new_value(ref.child("comments").child(post_id).get(), [])
    filter_comment = [item for item in comments if item["level"] == 1]
    limit_data = comments[offset : limit * (1 if offset == 0 else offset)]

    return {
        "total": len(filter_comment),
        "list": [
            {
                "item": item,
                "child": [
                    child
                    for child in comments
                    if child["level"] == 2 and child["parent"] == item["id"]
                ],
            }
            for item in limit_data
        ],
    }


async def send_comment(comment_payload: CommentPayload):
    ref = db.reference("social-network")

    comment_payload = comment_payload.model_dump()
    comment = comment_payload["comment"]
    post_id = comment_payload["post_id"]
    media_new = comment_payload["media_new"]

    media_list = await upload_media_db(media_new)

    comments = ref.child("comments").child(post_id).get()
    comments = new_value(comments, [])

    comment["id"] = str(uuid.uuid4())
    comments = [comment] + comments

    ref.child("comments").child(post_id).set(comments)
    ref.child("medias").child("comments").child(post_id).set(media_list)

    return comment


async def delete_comment(post_id: str, comment_id: str):
    ref = db.reference("social-network")

    comments = ref.child("comments").child(post_id).get()
    comments = [comment for comment in comments if comment["id"] != comment_id]

    ref.child("comments").child(post_id).set(comments)

    return True
