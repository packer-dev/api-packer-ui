from firebase_admin import db
from utils import find_index
import uuid
from models import Message, Group


async def getGroupByUser(userId: str):
    ref = db.reference("messenger")
    data = ref.get()

    groups = []
    if "groups" in data:
        groups = data["group"]

    groups = [
        item
        for item in groups
        if len([obj for obj in item["members"] if obj["user"]["id"] == userId]) > 0
    ]

    return groups


async def sendMessage(message: Message, group: Group):
    ref = db.reference("messenger")
    data = ref.get()

    groups = []
    if "groups" in data:
        groups = data["group"]
    message.id = uuid()
    group["messages"].append(message)
    if not group.id:
        group.id = uuid()
        groups.append(group.model_dump())
    else:
        index = find_index(groups, group.id)
        if index != -1:
            groups[index] = group.model_dump()

    data["groups"] = groups
    ref.set(data)

    return message


async def updateGroup(group: Group):
    ref = db.reference("messenger")
    data = ref.get()

    groups = []
    if "groups" in data:
        groups = data["group"]

    index = find_index(groups, group.id)
    if index != -1:
        groups[index] = group.model_dump()

    data["groups"] = groups
    ref.set(data)

    return group
