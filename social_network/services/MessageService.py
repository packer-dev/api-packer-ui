from firebase_admin import db
from utils import find_index
import uuid
from social_network.models import Group, SendMessageDTO


async def get_group_by_user(user_id: str):
    ref = db.reference("social-network")
    groups = ref.child("groups").get()

    if groups is None:
        groups = []

    groups = [
        item
        for item in groups
        if len([obj for obj in item["members"] if obj["user"]["id"] == user_id]) > 0
    ]

    return groups


async def get_messages_by_group(group_id: str):
    ref = db.reference("social-network")
    messages = ref.child("messages").child(group_id)

    return messages


async def send_message(dto: SendMessageDTO):
    ref = db.reference("social-network")

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

    group["last_message"] = message
    if group["id"] == "":
        group["id"] = str(uuid.uuid4())
        messages[group["id"]] = [message]
        groups.append(group)
    else:
        messages[group["id"]].append(message)

    group["last_message"] = message

    index = find_index(groups, group["id"])
    if index != -1:
        groups[index] = group

    ref.child("groups").set(groups)
    ref.child("messages").child(group["id"]).set(messages)

    return message


async def update_group(group: Group):
    ref = db.reference("social-network")
    groups = ref.child("groups").get()

    if groups is None:
        groups = []

    index = find_index(groups, group.id)
    if index != -1:
        groups[index] = group.model_dump()

    ref.child("groups").set(groups)

    return group


async def get_group_and_message_by_person(user_id: str, current_id: str):
    ref = db.reference("social-network")

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
                if member["user"]["id"] == user_id or member["user"]["id"] == current_id
            ]
        )
        == 2
    ]

    if len(item) == 0:
        return {"group": None, "messages": []}

    item = item[0]

    return {"group": item, "messages": await get_messages_by_group(item["id"])}
