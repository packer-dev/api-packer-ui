from fastapi import APIRouter, Form, UploadFile, File
from social_network.services.GroupService import (
    update_group,
    get_messages_by_group,
    upload_image_group,
    upload_info_group,
)
from social_network.models import Group
from typing import Optional

router = APIRouter(prefix="/api/social-network/v1/group")


@router.get("/update")
async def update_group_api(group: Group):
    return await update_group(group)


@router.get("/id")
async def get_messages_by_group_api(group_id: str):
    return await get_messages_by_group(group_id)


@router.post("/image")
async def upload_image_group_api(
    group_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    folder: str = Form(...),
    emoji: str = Form(...),
    name: str = Form(...),
):
    return await upload_image_group(
        group_id=group_id, file=file, folder=folder, emoji=emoji, name=name
    )


@router.post("/info")
async def upload_info_group_api(group: Group):
    return await upload_info_group(group)
