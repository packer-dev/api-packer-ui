import cloudinary
from cloudinary.uploader import upload
import io

# Configuration
cloudinary.config(
    cloud_name="ensonet-dev",
    api_key="625767877926127",
    api_secret="TSaPPlz96fO4w7hGf-Qtx3k25mo",  # Click 'View Credentials' below to copy your API secret
)


async def upload_cloudinary(file_contents: bytes):
    file_like_object = io.BytesIO(file_contents)
    result = cloudinary.uploader.upload(
        file_like_object, folder="FacebookNative", resource_type="image"
    )
    return result
