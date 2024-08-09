from fastapi import HTTPException
from social_network.models import FileDTO
from upload.app import upload_media_cloudinary, delete_media_cloudinary
from typing import List


async def upload_media(file_dto: FileDTO):
    try:
        contents = await file_dto.file.read()
        result = await upload_media_cloudinary(contents, file_dto.folder)
        media_url = result["secure_url"]
        return {"filename": file_dto.file.filename, "url": media_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_media(folder: List[str]):
    try:
        return await delete_media_cloudinary(folder)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
