from fastapi import APIRouter
from social_network.services.FacebookService import check_role_view_profile, test

router = APIRouter()


@router.get("/api/social-network/v1/profile/view")
async def check_role_view_profile_api(user1: str, user2: str):
    return check_role_view_profile(user1, user2)


@router.get("/api/social-network/v1/test")
async def test_api():
    return await test()
