from firebase_admin import db
from social_network.models import CommentPayload
from utils import new_value, upload_media_db
import uuid


async def send_comment(comment_payload: CommentPayload):
    ref = db.reference("social-network")

    comment, media_new, post_id = comment_payload.model_dump().values()

    media_list = upload_media_db(media_new)

    comments = ref.child("comments").child(post_id).get()
    comments = new_value(comments, [])

    comment["id"] = str(uuid.uuid4())
    comments.append(comment)

    ref.child("comments").child(post_id).set(comments)
    ref.child("medias").child("comments").child(post_id).set(media_list)

    return comment


async def delete_comment(post_id: str, comment_id: str):
    ref = db.reference("social-network")

    comments = ref.child("comments").child(post_id).get()
    comments = [comment for comment in comments if comment["id"] != comment_id]

    ref.child("comments").child(post_id).set(comments)

    return True
