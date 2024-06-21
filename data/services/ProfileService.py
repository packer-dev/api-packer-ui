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
    if type in result and idUser in result[type]:
        if idProfile != "":
            filter = []
            if type != "favorites" and type != "bags":
                filter = [obj for obj in result[type][idUser] if obj["id"] == idProfile]
            else:
                filter = [
                    obj
                    for obj in result[type][idUser]
                    if obj["product"]["id"] == idProfile
                ]
            data = filter[0] if len(filter) == 1 else None
            return data
        else:
            if idUser in result[type]:
                return [obj for obj in result[type][idUser]]
            else:
                return []
    else:
        return [] if idProfile == "" else None


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
        list = result[type][user["id"]] if user["id"] in result[type] else []
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

    id = data["id"] if type != "bags" and type != "favorites" else data["product"]["id"]

    if index == -1:
        return None
    if isNew:
        if type in user:
            user[type].append(id)
        else:
            user[type] = [data["id"]]
    if isDelete:
        user[type] = [obj for obj in user[type] if obj != id]

    result["users"][index] = user

    ref.set(result)
    return data
