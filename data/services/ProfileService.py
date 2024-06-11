from firebase_admin import db
import uuid
from data.models import ProfileDTO
import json


async def profileData(profile: ProfileDTO):
    profile = profile.model_dump()
    data = profile["data"]
    user = profile["user"]
    type = profile["type"]
    if data is None or user is None:
        return None

    ref = db.reference("data")
    result = ref.get()
    list = []
    if type in user:
        list = user[type]

    if data["id"] == "":
        data["id"] = str(uuid.uuid4())
        list.append(data)
    else:
        index = -1
        for pos, obj in enumerate(list):
            if obj["id"] == data["id"]:
                index = pos
                break
        if index == -1:
            return None
        list[index] = data

    index = -1

    for pos, obj in enumerate(result["users"]):
        if obj["id"] == user["id"]:
            index = pos
            break

    result["users"][index][type] = list

    ref.set(result)
    return data
