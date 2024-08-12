from firebase_admin import db
from utils import new_value, is_image, is_video, update_item, upload_media_db
import uuid
from social_network.models import PostPayload, FileDTO, Media
import os
from social_network.services.CommonServices import delete_media
from typing import Optional


async def get_post_by_id_user(user_id: str, is_profile: str):
    ref = db.reference("social-network")

    posts = ref.child("posts").get()
    relationships = ref.child("relationships").get()

    if posts is None or relationships is None:
        return []

    response = []

    if is_profile == "false":
        relationships = [
            relationship["user2"]
            for relationship in relationships
            if relationship["user1"] == user_id
        ]

        for relationship in relationships:
            list_post = [
                {
                    "post": post,
                    "medias": new_value(
                        ref.child("medias").child("posts").child(post["id"]).get(), []
                    ),
                }
                for post in posts
                if post["user"]["id"] == relationship
            ]
            response = response + list_post
    else:
        response = [
            {
                "post": post,
                "medias": new_value(
                    ref.child("medias").child("posts").child(post["id"]).get(), []
                ),
            }
            for post in posts
            if post["user"]["id"] == user_id
        ]

    # sort by time

    # sort by time
    return response


async def create_post(post_payload: PostPayload):
    try:
        ref = db.reference("social-network")

        post = post_payload.post.model_dump()
        media_new = post_payload.media_new

        post["id"] = str(uuid.uuid4())
        posts = ref.child("posts").get()

        media_list = []

        print(media_new)
        if media_new is not None:
            if len(media_new) > 0:
                media_list = await upload_media_db(media_new)
            else:
                return ""
        if posts is None:
            ref.child("posts").set([post])
        else:
            posts.append(post)
            ref.child("posts").set(posts)

        ref.child("medias").child("posts").child(post["id"]).set(media_list)

        return post

    except OSError as err:
        print("OS error:", err)


async def edit_post(post_payload: PostPayload):
    ref = db.reference("social-network")

    post = post_payload.post.model_dump()
    media_new = post_payload.media_new
    media_old = [child.model_dump() for child in post_payload.media_old]

    media_list = media_old

    get_media_old = ref.child("medias").child("posts").child(post["id"]).get()
    get_media_old = new_value(get_media_old, [])

    delete_public_ids = []

    for item in get_media_old:
        check = [child for child in media_old if child["id"] == item["id"]]
        if len(check) == 0:
            folder = item["folder"]
            url = item["url"]
            public_id = os.path.splitext(
                url[url.find(f"FacebookNative/{(folder)}/") : len(url)]
            )[0]
            delete_public_ids.append(public_id)
    if len(delete_public_ids) > 0:
        await delete_media(delete_public_ids)

    if len(media_new) > 0:
        media_new = await upload_media_db(media_new)
        media_list = media_list + media_new

    posts = new_value(ref.child("posts").get(), [])
    posts = update_item(posts, post)

    ref.child("medias").child("posts").child(post["id"]).set(media_list)
    ref.child("posts").set(posts)

    return post


async def delete_post(post_id: str):
    ref = db.reference("social-network")

    posts = new_value(ref.child("posts").get(), [])
    media_post = new_value(ref.child("medias").child("posts").child(post_id).get(), [])
    media_comment = new_value(
        ref.child("medias").child("comments").child(post_id).get(), []
    )

    medias = media_post + media_comment
    if len(medias) > 0:
        public_ids = []
        for media in medias:
            url = media["url"]
            folder = media["folder"]
            public_id = os.path.splitext(
                url[url.find(f"FacebookNative/{(folder)}/") : len(url)]
            )[0]
            public_ids.append(public_id)

        await delete_media(public_ids)

    posts = [post for post in posts if post["id"] != post_id]

    ref.child("medias").child("posts").child(post_id).set({})
    ref.child("medias").child("comments").child(post_id).set({})
    ref.child("comments").child(post_id).set({})
    ref.child("posts").set(posts)
    return True
