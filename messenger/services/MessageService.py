from firebase_admin import db
from utils import find_index
import uuid
from messenger.models import Group, SendMessageDTO


async def getGroupByUser(userId: str):
    ref = db.reference("messenger")
    data = ref.get()

    groups = []
    if "groups" in data:
        groups = data["groups"]

    groups = [
        item
        for item in groups
        if len([obj for obj in item["members"] if obj["user"]["id"] == userId]) > 0
    ]

    return groups


async def getMessagesByGroup(groupId: str):
    ref = db.reference("messenger")
    data = ref.get()

    if data is None:
        return []

    list = []
    if "messages" in data:
        list = [] if groupId not in data["messages"] else data["messages"][groupId]

    return list


async def sendMessage(dto: SendMessageDTO):
    ref = db.reference("messenger")
    data = ref.get()

    dto = dto.model_dump()

    message = dto["message"]
    group = dto["group"]

    groups = []
    if "groups" in data:
        groups = data["groups"]

    messages = {}
    if "messages" in data:
        messages = data["messages"]
    message["id"] = str(uuid.uuid4())

    group["lastMessage"] = message
    if not group["id"]:
        group["id"] = str(uuid.uuid4())
        messages[group["id"]] = [message]
    else:
        messages[group["id"]].append(message)

    groups.append(group)
    data["groups"] = groups
    data["messages"] = messages
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
