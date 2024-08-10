from fastapi import APIRouter
from social_network.models import LoginDTO, User
from social_network.services.AuthServices import (
    login,
    register,
    get_user_by_id,
    get_friends,
    update_user_service
)

router = APIRouter()


@router.post("/api/social-network/v1/login")
async def login_api(dto: LoginDTO):
    return await login(dto)


@router.post("/api/social-network/v1/register")
async def register_api(dto: User):
    return await register(dto)

@router.put("/api/social-network/v1/user")
async def register_api(dto: User):
    return await update_user_service(dto)

@router.get("/api/social-network/v1/user/id")
async def get_user_by_id_api(user_id: str):
    return await get_user_by_id(user_id)


@router.get("/api/social-network/v1/friends")
async def get_friends_api(user_id: str):
    return await get_friends(user_id)
