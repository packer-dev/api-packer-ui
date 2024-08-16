from fastapi import APIRouter
from social_network.models import SendMessageDTO, Group
from social_network.services.MessageService import (
    send_message,
    get_group_by_user,
    update_group,
    get_messages_by_group,
    get_group_and_message_by_person,
    update_status_message,
    get_amount_message_not_read,
)

router = APIRouter()


@router.post("/api/social-network/v1/message/send")
async def send_message_api(dto: SendMessageDTO):
    return await send_message(dto)


@router.get("/api/social-network/v1/message/list")
async def get_group_by_user_api(user_id: str):
    return await get_group_by_user(user_id)


@router.get("/api/social-network/v1/group/update")
async def update_group_api(group: Group):
    return await update_group(group)


@router.get("/api/social-network/v1/group/id")
async def get_messages_by_group_api(group_id: str):
    return await get_messages_by_group(group_id)


@router.get("/api/social-network/v1/message/get-child")
async def get_group_and_message_by_person_api(user_id: str, current_id: str):
    return await get_group_and_message_by_person(user_id, current_id)


@router.get("/api/social-network/v1/message/update")
async def update_status_message_api(group_id):
    return await update_status_message(group_id)


@router.get("/api/social-network/v1/message/status")
async def get_amount_message_not_read_api(user_id):
    return await get_amount_message_not_read(user_id)
