from fastapi import APIRouter
from social_network.services.FacebookService import (
    check_role_view_profile,
    get_navbar_amount_new,
)

router = APIRouter(prefix="/api/social-network/v1")


@router.get("/profile/view")
async def check_role_view_profile_api(user1: str, user2: str):
    return await check_role_view_profile(user1, user2)


@router.get("/navbar/amount")
async def get_navbar_amount_new_api(user_id: str):
    return await get_navbar_amount_new(user_id)
