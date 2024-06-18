from firebase_admin import db
import uuid
from data.models import ProfileDTO, GetProfileDTO
from utils import find_index


async def getProfileData(profile: GetProfileDTO):
    profile = profile.model_dump()
    idUser = profile["idUser"]
    type = profile["type"]

    ref = db.reference("data")
    result = ref.get()
    if type in result:
        if idUser in result[type]:
            return [obj for obj in result[type][idUser]]
        else:
            return []
    else:
        return []


async def profileData(profile: ProfileDTO):
    profile = profile.model_dump()
    data = profile["data"]
    type = profile["type"]
    user = profile["user"]
    isDelete = profile["isDelete"]

    if data is None:
        return None

    ref = db.reference("data")
    result = ref.get()

    list = []

    isNew = data["id"] == ""

    if type in result:
        list = result[type][user["id"]]
    if isDelete:
        list = [obj for obj in list if obj["id"] != data["id"]]
    else:
        if data["id"] == "":
            data["id"] = str(uuid.uuid4())
            list.append(data)
        else:
            index = find_index(list, data["id"])
            if index == -1:
                return None
            list[index] = data
    if type not in result:
        result[type] = {}
    result[type][user["id"]] = list

    index = find_index(result["users"], user["id"])

    if index != -1:
        if isNew:
            if type in user:
                user[type].append(
                    data["id"]
                    if type != "bags" and type != "favorites"
                    else data["product"]["id"]
                )
            else:
                user[type] = [data["id"]]
        result["users"][index] = user

    ref.set(result)
    return data
