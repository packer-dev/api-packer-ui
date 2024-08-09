import cloudinary
from cloudinary import uploader, api
import io


# Configuration
cloudinary.config(
    cloud_name="ensonet-dev",
    api_key="625767877926127",
    api_secret="TSaPPlz96fO4w7hGf-Qtx3k25mo",  # Click 'View Credentials' below to copy your API secret
)


async def upload_media_cloudinary(file_contents: bytes, folder: str):
    file_like_object = io.BytesIO(file_contents)
    result = uploader.upload(file_like_object, folder=folder, resource_type="image")
    return result


async def delete_media_cloudinary(folder: str):
    return api.delete_resources(folder)
