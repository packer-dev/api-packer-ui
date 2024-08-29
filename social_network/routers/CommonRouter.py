from fastapi import APIRouter, UploadFile, File, Form
from social_network.services.CommonServices import upload_media, delete_media
from social_network.models import FileDTO
from typing import List

router = APIRouter(prefix="/api/social-network/v1")


@router.post("/upload/media")
async def upload_media_api(folder: str = Form(...), file: UploadFile = File(...)):
    file_dto = FileDTO(file=file, folder=folder)
    return await upload_media(file_dto)


@router.delete("/delete/media")
async def delete_media_api(folder: List[str]):
    return await delete_media(folder)
