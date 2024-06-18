from firebase_admin import db
import uuid
from data.models import ProfileDTO, GetProfileDTO
from utils import find_index


async def getProfileData(profile: GetProfileDTO):
    profile = profile.model_dump()
    idUser = profile["idUser"]
    idProfile = profile["idProfile"]
    type = profile["type"]

    ref = db.reference("data")
    result = ref.get()

    list = result[type][idUser]
    index = find_index(list, idProfile)
    if index == -1:
        return None

    return list[index]


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

    index = find_index(result["users"], user["id"])

    if index != -1:
        user[type] = (
            int(user[type]) + 1
            if data["id"] == "" or data["id"] is None
            else int(user[type]) - 1 if isDelete == True else int(user[type])
        )
        result["users"][index] = user

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

    ref.set(result)
    return data
