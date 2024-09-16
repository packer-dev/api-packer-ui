from firebase_admin import db
from utils import new_value, update_item, upload_media_db, get_info_user
import uuid
from social_network.models import PostPayload
import os
from social_network.services.CommonServices import delete_media
from social_network.services.AuthServices import get_friend_main
from datetime import datetime
from concurrent import futures


def update_user_post(users, post):
    post["user"] = get_info_user(users, post["user"]["id"])
    return post


async def get_post_by_id_user(
    user_id: str, is_profile: str, offset: int = 0, limit: int = 10
):
    ref = db.reference("social-network")

    posts = ref.child("posts").get()
    relationships = ref.child("relationships").get()
    feel_post = ref.child("feel-post").get()
    users = new_value(ref.child("users").get(), [])
    media_post = new_value(ref.child("medias").child("posts").get(), [])
    comments = new_value(ref.child("comments").get(), [])

    if posts is None and relationships is None:
        return []

    response = []
    if is_profile == "false":
        relationships = [
            relationship["user2"]
            for relationship in relationships
            if relationship["user1"] == user_id and relationship["status"] == 3
        ]

        for relationship in relationships:
            filter_post = [post for post in posts if post["user"]["id"] == relationship]
            response = response + filter_post

    else:
        response = [post for post in posts if post["user"]["id"] == user_id]

    # Assuming each item has a datetime field in ISO format
    sorted_data = sorted(response, key=lambda x: x["time_created"], reverse=True)
    sorted_data = [
        {
            "post": update_user_post(users, post),
            "medias": new_value(media_post.get(post["id"]), []),
            "feel": (
                feel_post[post["id"]]
                if feel_post is not None and post["id"] in feel_post
                else []
            ),
            "comment": len(new_value(comments.get(post["id"]), [])),
        }
        for post in sorted_data
    ]
    sorted_data = sorted_data[offset : limit * (1 if offset == 0 else offset)]
    return {"total": len(sorted_data), "list": sorted_data}


async def create_post(post_payload: PostPayload):
    try:
        ref = db.reference("social-network")
        users = ref.child("users").get()

        post = post_payload.post.model_dump()
        media_new = post_payload.media_new

        post["id"] = str(uuid.uuid4())
        post["time_created"] = str(datetime.now())
        posts = ref.child("posts").get()

        media_list = []

        if media_new is not None and len(media_new) > 0:
            media_list = await upload_media_db(media_new)

        if posts is None:
            ref.child("posts").set([post])
        else:
            posts = [post] + posts
            ref.child("posts").set(posts)

        ref.child("medias").child("posts").child(post["id"]).set(media_list)

        return {
            "post": update_user_post(users, post),
            "medias": media_list,
            "feel": [],
            "comment": [],
        }

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

    if media_new is not None:
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


async def get_post_by_id(post_id: str):
    ref = db.reference("social-network")
    posts = new_value(ref.child("posts").get(), [])
    users = new_value(ref.child("users").get(), [])
    posts = [post for post in posts if post["id"] == post_id]
    response = posts[0] if len(posts) == 1 else None
    if response is None:
        return None

    return {
        "post": update_user_post(users, response),
        "medias": new_value(
            ref.child("medias").child("posts").child(response["id"]).get(), []
        ),
        "feel": new_value(ref.child("feel-post").child(post_id).get(), []),
    }


async def get_user_feel_by_post(post_id: str):
    ref = db.reference("social-network")
    feels = new_value(ref.child("feel-post").child(post_id).get(), [])
    users = new_value(ref.child("users").get(), [])
    response = []
    for feel in feels:
        user = [item for item in users if item["id"] == feel]
        user = None if len(user) == 0 else user[0]
        if user is not None:
            response.append(user)

    return response


async def send_user_feel_by_post(post_id: str, user_id: str, type: int):
    ref = db.reference("social-network")
    feels = new_value(ref.child("feel-post").child(post_id).get(), [])
    users = new_value(ref.child("users").get(), [])
    index = -1
    user = [item for item in users if item["id"] == user_id]
    user = user[0] if len(user) == 1 else None
    new_feel = {"id": str(uuid.uuid4()), "type": type, "user": user}
    for pos in range(len(feels)):
        if feels[pos]["user"]["id"] == user_id:
            index = pos
    is_add = new_feel
    if index == -1:
        feels.append(new_feel)
    else:
        if feels[index]["type"] == type:
            feels = [feel for feel in feels if feel["user"]["id"] != user_id]
            is_add = None
        else:
            feels[index]["type"] = type
            is_add = feels[index]
    ref.child("feel-post").child(post_id).set(feels)

    return is_add


async def get_media(user_id, type, limit=9, offset=0):
    ref = db.reference("social-network")

    posts = new_value(ref.child("posts").get(), [])
    if len(posts) == 0:
        return []

    response = []

    if type == 0:
        response = await get_friend_main(user_id, 3)

    else:
        response = []
        posts = [post for post in posts if post["user"]["id"] == user_id]
        sorted_data = sorted(posts, key=lambda x: x["time_created"], reverse=True)
        for post in sorted_data:
            medias = new_value(
                ref.child("medias").child("posts").child(post["id"]).get(), []
            )
            for media in medias:
                if media["type"] == type:
                    response.append(
                        {
                            "post_id": post["id"],
                            "user_id": post["user"]["id"],
                            "media": media,
                        }
                    )

    return {
        "list": response[offset : limit * (1 if offset == 0 else offset)],
        "total": len(response),
    }
