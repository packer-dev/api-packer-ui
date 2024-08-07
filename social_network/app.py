from fastapi import APIRouter
from social_network.models import LoginDTO, User, SendMessageDTO, Group
from social_network.services.AuthServices import (
    login,
    register,
    get_user_by_id,
    get_friends,
)
from social_network.services.MessageService import (
    send_message,
    get_group_by_user,
    update_group,
    get_messages_by_group,
    get_group_and_message_by_person,
)

router = APIRouter()


@router.post("/api/messenger/v1/login")
async def login_api(dto: LoginDTO):
    return await login(dto)


@router.post("/api/messenger/v1/register")
async def register_api(dto: User):
    return await register(dto)


@router.get("/api/messenger/v1/user/id")
async def get_user_by_id_api(user_id: str):
    return await get_user_by_id(user_id)


@router.post("/api/messenger/v1/message/send")
async def send_message_api(dto: SendMessageDTO):
    return await send_message(dto)


@router.get("/api/messenger/v1/message/list")
async def get_group_by_user_api(user_id: str):
    return await get_group_by_user(user_id)


@router.get("/api/messenger/v1/group/update")
async def update_group_api(group: Group):
    return await update_group(group)


@router.get("/api/messenger/v1/group/id")
async def get_messages_by_group_api(group_id: str):
    return await get_messages_by_group(group_id)


@router.get("/api/messenger/v1/friends")
async def get_friends_api(user_id: str):
    return await get_friends(user_id)


@router.get("/api/messenger/v1/message/get-child")
async def get_group_and_message_by_person_api(user_id: str, current_id: str):
    return await get_group_and_message_by_person(user_id, current_id)
