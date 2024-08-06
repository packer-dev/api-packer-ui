from firebase_admin import db
from utils import find_index
import uuid
from messenger.models import Group, SendMessageDTO


async def getGroupByUser(userId: str):
    ref = db.reference("messenger")
    groups = ref.child("groups").get()

    if groups is None:
        groups = []

    groups = [
        item
        for item in groups
        if len([obj for obj in item["members"] if obj["user"]["id"] == userId]) > 0
    ]

    return groups


async def getMessagesByGroup(groupId: str):
    ref = db.reference("messenger")
    messages = ref.child("messages").child(groupId)

    return messages


async def sendMessage(dto: SendMessageDTO):
    ref = db.reference("messenger")

    dto = dto.model_dump()
    message = dto["message"]
    group = dto["group"]

    groups = ref.child("groups").get()
    messages = ref.child("messages").get()

    if groups is None:
        groups = []

    if messages is None:
        messages = {}

    message["id"] = str(uuid.uuid4())

    group["lastMessage"] = message
    if group["id"] == "":
        group["id"] = str(uuid.uuid4())
        messages[group["id"]] = [message]
        groups.append(group)
    else:
        messages[group["id"]].append(message)

    group["lastMessage"] = message

    index = find_index(groups, group["id"])
    if index != -1:
        groups[index] = group

    ref.child("groups").set(groups)
    ref.child("messages").child(group["id"]).set(messages)

    return message


async def updateGroup(group: Group):
    ref = db.reference("messenger")
    groups = ref.child("groups").get()

    if groups is None:
        groups = []

    index = find_index(groups, group.id)
    if index != -1:
        groups[index] = group.model_dump()

    ref.child("groups").set(groups)

    return group


async def getGroupAndMessageByPerson(userId: str, currentId: str):
    ref = db.reference("messenger")

    groups = ref.child("groups").get()
    if groups is None:
        return {"group": None, "messages": []}

    item = [
        group
        for group in groups
        if len(group["members"]) == 2
        and len(
            [
                member
                for member in group["members"]
                if member["user"]["id"] == userId or member["user"]["id"] == currentId
            ]
        )
        == 2
    ]

    if len(item) == 0:
        return {"group": None, "messages": []}

    item = item[0]

    return {"group": item, "messages": await getMessagesByGroup(item["id"])}
