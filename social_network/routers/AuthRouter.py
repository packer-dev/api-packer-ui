from fastapi import APIRouter
from social_network.models import LoginDTO, User, RelationshipPayload
from social_network.services.AuthServices import (
    login,
    register,
    get_user_by_id,
    get_friends,
    update_user_service,
    get_suggest_friend,
    relationship_request,
    upload_media_profile_user,
    relationship_check,
    get_friend_main,
)
from fastapi import Form, UploadFile, File

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


@router.get("/api/social-network/v1/suggest-friend")
async def get_suggest_friend_api(user_id: str):
    return await get_suggest_friend(user_id)


@router.post("/api/social-network/v1/relationship")
async def relationship_api(relationship_payload: RelationshipPayload):
    return await relationship_request(relationship_payload)


@router.get("/api/social-network/v1/relationship")
async def relationship_api(user1: str, user2: str):
    return await relationship_check(user1, user2)


@router.get("/api/social-network/v1/users")
async def relationship_api(user_id: str, status: int):
    return await get_friend_main(user_id, status)


@router.post("/api/social-network/v1/upload-profile")
async def upload_media_profile_user_api(
    folder: str = Form(...),
    file: UploadFile = File(None),
    is_cover: str = Form(...),
    user_id: str = Form(...),
):
    return await upload_media_profile_user(
        folder=folder, file=file, is_cover=is_cover, user_id=user_id
    )
