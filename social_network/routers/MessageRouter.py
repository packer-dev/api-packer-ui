from fastapi import APIRouter
from social_network.models import SendMessageDTO, Group
from social_network.services.MessageService import (
    send_message,
    get_group_by_user,
    get_group_and_message_by_person,
    update_status_message,
    get_amount_message_not_read,
)

router = APIRouter(prefix="/api/social-network/v1/message")


@router.post("/send")
async def send_message_api(dto: SendMessageDTO):
    return await send_message(dto)


@router.get("/list")
async def get_group_by_user_api(user_id: str):
    return await get_group_by_user(user_id)


@router.get("/get-child")
async def get_group_and_message_by_person_api(user_id: str, current_id: str):
    return await get_group_and_message_by_person(user_id, current_id)


@router.get("/update")
async def update_status_message_api(group_id, user_id):
    return await update_status_message(group_id, user_id)


@router.get("/status")
async def get_amount_message_not_read_api(user_id):
    return await get_amount_message_not_read(user_id)
