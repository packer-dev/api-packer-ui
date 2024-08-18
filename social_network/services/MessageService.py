from firebase_admin import db
from utils import new_value, get_info_user, update_item
import uuid
from social_network.models import Group, SendMessageDTO


async def get_group_by_user(user_id: str):
    ref = db.reference("social-network")
    groups = new_value(ref.child("groups").get(), [])
    users = new_value(ref.child("users").get(), [])

    groups = [
        update_member_group(users, item)
        for item in groups
        if len([obj for obj in item["members"] if obj["user"]["id"] == user_id]) > 0
    ]

    return groups


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
    messages = new_value(ref.child("messages").child(group_id).get(), [])

    if len(messages) > 0:
        for i in range(len(messages) - 1, -1, -1):
            if messages[i]["user"]["id"] != user_id and messages[i]["is_read"] == False:
                messages[len(messages) - 1]["status"] = True
                ref.child("messages").child(group_id).set(messages)
                return True
    return False


async def get_amount_message_not_read(user_id):
    ref = db.reference("social-network")

    groups = await get_group_by_user(user_id)
    response = []
    for group in groups:
        messages = new_value(ref.child("messages").child(group["id"]).get(), [])
        if len(messages) > 0:
            is_read = True
            for i in range(len(messages) - 1, -1, -1):
                if (
                    messages[i]["user"]["id"] != user_id
                    and messages[i]["is_read"] == False
                ):
                    is_read = False
                    break
            if is_read == False:
                response.append(group)
    return len(response)
