from fastapi import APIRouter, UploadFile, File, Form
from social_network.services.CommonServices import upload_media, delete_media
from social_network.models import FileDTO
from typing import List

router = APIRouter()


@router.post("/api/social-network/v1/upload/media")
async def upload_media_api(folder: str = Form(...), file: UploadFile = File(...)):
    file_dto = FileDTO(file=file, folder=folder)
    return await upload_media(file_dto)


@router.delete("/api/social-network/v1/delete/media")
async def delete_media_api(folder: List[str]):
    return await delete_media(folder)
