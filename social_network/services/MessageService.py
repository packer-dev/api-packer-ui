from firebase_admin import db
from utils import new_value, get_info_user, update_item, find_index
import uuid
from social_network.models import Group, SendMessageDTO
from datetime import datetime


async def get_group_by_user(user_id: str):
    ref = db.reference("social-network")
    groups = new_value(ref.child("groups").get(), [])
    users = new_value(ref.child("users").get(), [])

    groups = [
        update_member_group(users, item)
        for item in groups
        if len([obj for obj in item["members"] if obj["user"]["id"] == user_id]) > 0
    ]

    sorted_data = sorted(
        groups, key=lambda x: x["last_message"]["time_created"], reverse=True
    )

    return sorted_data


async def get_messages_by_group(group_id: str):
    ref = db.reference("social-network")
    messages = new_value(ref.child("messages").child(group_id).get(), [])
    users = new_value(ref.child("users").get(), [])

    for message in messages:
        message["user"] = get_info_user(users, message["user"]["id"])
    return messages


async def send_message(dto: SendMessageDTO):
    ref = db.reference("social-network")

    message, group = dto.model_dump().values()

    groups = new_value(ref.child("groups").get(), [])
    messages = []

    group["last_message"] = message
    group["last_time_update"] = str(datetime.now())
    group["time_created"] = str(datetime.now())

    if group["id"] == "":
        group["id"] = str(uuid.uuid4())
        groups.append(group)
    else:
        messages = new_value(ref.child("messages").child(group["id"]).get(), [])
        groups = update_item(groups, group)
    messages.append(message)
    ref.child("groups").set(groups)
    ref.child("messages").child(group["id"]).set(messages)

    return {"message": message, "group": group}


async def update_group(group: Group):
    ref = db.reference("social-network")
    groups = new_value(ref.child("groups").get(), [])
    groups = update_item(groups, group.model_dump())

    ref.child("groups").set(groups)
    return group


async def get_group_and_message_by_person(user_id: str, current_id: str):
    ref = db.reference("social-network")

    groups = ref.child("groups").get()
    users = new_value(ref.child("users").get(), [])

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

    item = update_member_group(users, item[0])

    messages = await get_messages_by_group(item["id"])

    return {"group": item, "messages": messages}


def update_member_group(users, group):
    if "members" in group:
        for index in range(len(group["members"])):
            group["members"][index]["user"] = get_info_user(
                users, group["members"][index]["user"]["id"]
            )
        group["last_message"]["user"] = get_info_user(
            users, group["last_message"]["user"]["id"]
        )
    return group


async def update_status_message(group_id, user_id):
    ref = db.reference("social-network")
    groups = new_value(ref.child("groups").get(), [])

    index = find_index(groups, group_id)
    if index == -1:
        return False

    groups[index]["seen"][user_id] = True
    ref.child("groups").set(groups)

    return True


async def get_amount_message_not_read(user_id):
    groups = await get_group_by_user(user_id)
    count = 0
    for group in groups:
        status = group["seen"][user_id] if user_id in group["seen"] else True
        if status == False:
            count = count + 1
    return count
