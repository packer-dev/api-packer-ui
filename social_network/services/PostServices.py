from firebase_admin import db
from utils import find_index
import uuid
from social_network.models import Post


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
            list_post = [post for post in posts if post["user"]["id"] == relationship]
            response = response + list_post
    else:
        response = [post for post in posts if post["user"]["id"] == user_id]

    # sort by time

    # sort by time
    return response


async def create_post(post: Post):
    ref = db.reference("social-network")

    post = post.model_dump()
    post["id"] = str(uuid.uuid4())
    posts = ref.child("posts").get()

    if posts is None:
        ref.child("posts").set([post])
    else:
        posts.append(post)
        ref.child("posts").set(posts)
    return post
