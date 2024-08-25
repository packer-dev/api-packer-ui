import hashlib
import os
from social_network.models import FileDTO, Media
from social_network.services.CommonServices import upload_media
import uuid
from social_network.dto.response import user_response


def find_index(list, id):
    index = -1
    for _, item in enumerate(list):
        if str(item["id"]) == str(id):
            return _
    return index


def update_item(items, new_item):
    index = find_index(items, new_item["id"])
    if index != -1:
        items[index] = new_item
    return items


def md5(password: str) -> str:
    hashed_password = hashlib.md5(password.encode("utf-8"))

    return hashed_password.hexdigest()


def find_by_id(items, id):
    items = [user for user in items if user["id"] == id]
    return None if len(items) == 0 else items[0]


def new_value(item, default_value):
    return default_value if item is None else item


import os


def is_image(filename):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    return os.path.splitext(filename)[1].lower() in image_extensions


def is_video(filename):
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
    return os.path.splitext(filename)[1].lower() in video_extensions


async def upload_media_db(media_new):
    if media_new is None:
        return []

    media_list = []

    for media in media_new:
        folder = "Other"
        if is_image(media.filename):
            folder = "Images"
        if is_video(media.filename):
            folder = "Videos"

        file_dto = FileDTO(file=media, folder=f"/FacebookNative/{folder}")
        result = await upload_media(file_dto)
        if result:
            media_db = Media(
                id=str(uuid.uuid4()),
                folder=folder,
                status=1,
                type=1,
                url=result["url"],
            )
            media_list.append(media_db.model_dump())

    return media_list


def get_info_user(users, id):
    index = find_index(users, id)
    if index == -1:
        return None
    else:
        return user_response(users[index])
