from firebase_admin import db
from utils import new_value, update_item
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
    messages = ref.child("messages").child(group_id).get()

    return messages


async def send_message(dto: SendMessageDTO):
    ref = db.reference("social-network")

    message, group = dto.model_dump().values()

    groups = new_value(ref.child("groups").get(), [])
    messages = new_value(ref.child("messages").get(), {})

    message["id"] = str(uuid.uuid4())

    group["last_message"] = message
    if group["id"] == "":
        group["id"] = str(uuid.uuid4())
        messages[group["id"]] = [message]
        groups.append(group)
    else:
        messages[group["id"]].append(message)
        groups = update_item(groups, group)

    ref.child("groups").set(groups)
    ref.child("messages").child(group["id"]).set(messages)

    return message


async def update_group(group: Group):
    ref = db.reference("social-network")
    groups = new_value(ref.child("groups").get(), [])
    groups = update_item(groups, group.model_dump())

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

    messages = await get_messages_by_group(item["id"])

    return {"group": item, "messages": messages}
