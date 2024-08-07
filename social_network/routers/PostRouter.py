from fastapi import APIRouter
from social_network.services.PostServices import get_post_by_id_user, create_post
from social_network.models import Post

router = APIRouter()


@router.get("/api/social-network/v1/post")
async def get_post_by_id_user_api(user_id: str, is_profile: str):
    return await get_post_by_id_user(user_id, is_profile)


@router.post("/api/social-network/v1/post")
async def create_post_api(post: Post):
    return await create_post(post)
