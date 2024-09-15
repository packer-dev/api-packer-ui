from social_network.models import (
    User,
    LoginDTO,
    RelationshipPayload,
    Relationship,
    FileDTO,
    Post,
    Media,
    ContentPost,
)
from firebase_admin import db
from utils import md5, find_index, find_by_id, new_value
import uuid
from datetime import datetime
from social_network.services.CommonServices import upload_media, delete_media
import os
from social_network.dto.response import user_response
from typing import List


async def get_user_by_id(id: str):
    ref = db.reference("social-network")
    users = new_value(ref.child("users").get(), [])
    user = find_by_id(users, id)

    return user_response(user)


async def login(login_dto: LoginDTO):
    ref = db.reference("social-network")
    users = new_value(ref.child("users").get(), [])
    for obj in users:
        if obj["email"] == login_dto.email and obj["password"] == md5(
            login_dto.password
        ):
            index = find_index(users, obj["id"])
            users[index]["last_time_active"] = str(datetime.now())
            ref.child("users").set(users)
            return user_response(users[index])

    return None


def check_exist_account(user: User, users: list[User]):
    for obj in users:
        if obj["email"] == user.email:
            return True

    return False


async def register(user: User):
    ref = db.reference("social-network")
    users = new_value(ref.child("users").get(), [])
    user.password = md5(user.password)
    user.id = str(uuid.uuid4())
    user.time_created = str(datetime.now())
    user.last_time_active = str(datetime.now())

    check_account = check_exist_account(user, users)
    if check_account:
        return {"status": 1, "message": "Email exist in system!"}

    users.append(user.model_dump())
    ref.child("users").set(users)
    return user_response(user.model_dump())


async def update_user_service(user: User):
    ref = db.reference("social-network")
    users = new_value(ref.child("users").get(), [])
    index = find_index(users, user.id)
    if index == -1:
        return None

    users[index] = user.model_dump()

    ref.child("users").set(users)
    return user_response(users[index])


def get_friend_by_id(relationships, users, user_id):
    relationships = [
        relationship
        for relationship in relationships
        if relationship["user1"] == user_id and relationship["status"] == 3
    ]

    response = []

    for relationship in relationships:
        index = find_index(users, relationship["user2"])
        if index != -1:
            response.append(user_response(users[index]))

    return response


async def get_friends(user_id: str, selected: List[str] = None):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    relationships = ref.child("relationships").get()

    if users is None or relationships is None:
        return []

    friends = get_friend_by_id(relationships, users, user_id)
    response = []
    for item in friends:
        check = (
            [{}]
            if len(selected) == 0
            else [child for child in selected if child == item["id"]]
        )
        if len(check) > 0:
            response.append(item)
    return response


def get_manual_friend(relationships, users, user1, user2):
    friend_user_1 = get_friend_by_id(relationships, users, user1)
    friend_user_1 = {user["id"] for user in friend_user_1}
    friend_user_2 = get_friend_by_id(relationships, users, user2)
    friend_user_2 = {user["id"] for user in friend_user_2}
    return len(friend_user_1.intersection(friend_user_2))


def check_relationship_by_user(relationships, user1, user2):
    relationships = [
        item
        for item in relationships
        if item["user1"] == user1 and item["user2"] == user2
    ]
    relationships = relationships[0]["status"] if len(relationships) > 0 else 0
    return relationships


async def get_suggest_friend(user_id: str):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    relationships = new_value(ref.child("relationships").get(), [])

    if users is None:
        return []

    friends = get_friend_by_id(relationships, users, user_id)
    response = []

    for user in users:
        index = find_index(friends, user["id"])
        if index == -1 and user["id"] != user_id:
            response.append(user_response(user))
    return [
        {
            "user": item,
            "manual": get_manual_friend(
                relationships=relationships,
                users=users,
                user1=user_id,
                user2=item["id"],
            ),
            "status": check_relationship_by_user(
                relationships=relationships, user1=user_id, user2=item["id"]
            ),
        }
        for item in response
    ]


def get_status_relationship(status):
    status1 = 0
    status2 = 0
    if status == "send":
        status1 = 1
        status2 = 2
    elif status == "accept":
        status1 = 3
        status2 = 3
    return {"status1": status1, "status2": status2}


def process_status_relationship(
    relationships, status1, status2, user1, user2, get_user1, get_user2
):
    new_relationships = []

    if get_user1 is None:
        get_user1 = Relationship(
            id=str(uuid.uuid4()), user1=user1, user2=user2, status=status1
        )
        if status1 != 0:
            new_relationships.append(get_user1.model_dump())
    else:
        index = find_index(relationships, get_user1["id"])
        if index != -1:
            relationships[index]["status"] = status1

    if get_user2 is None:
        get_user2 = Relationship(
            id=str(uuid.uuid4()), user1=user2, user2=user1, status=status2
        )
        if status2 != 0:
            new_relationships.append(get_user2.model_dump())
    else:
        index = find_index(relationships, get_user2["id"])
        if index != -1:
            relationships[index]["status"] = status2

    return new_relationships


async def relationship_request(relationship_payload: RelationshipPayload):
    user1, user2, status = relationship_payload.model_dump().values()

    ref = db.reference("social-network")
    relationships = new_value(ref.child("relationships").get(), [])

    get_status = get_status_relationship(status)
    status1 = get_status["status1"]
    status2 = get_status["status2"]

    get_user1 = [
        item
        for item in relationships
        if (item["user1"] == user1 and item["user2"] == user2)
    ]
    get_user1 = None if len(get_user1) == 0 else get_user1[0]
    get_user2 = [
        item
        for item in relationships
        if (item["user1"] == user2 and item["user2"] == user1)
    ]
    get_user2 = None if len(get_user2) == 0 else get_user2[0]

    new_relationships = process_status_relationship(
        relationships=relationships,
        status1=status1,
        status2=status2,
        user1=user1,
        user2=user2,
        get_user1=get_user1,
        get_user2=get_user2,
    )

    if status == "":
        relationships = [
            item
            for item in relationships
            if get_user1["id"] != item["id"] and get_user2["id"] != item["id"]
        ]

    ref.child("relationships").set(relationships + new_relationships)

    return True


async def upload_media_profile_user(folder, file, is_cover, user_id):
    ref = db.reference("social-network")

    users = new_value(ref.child("users").get(), [])
    posts = new_value(ref.child("posts").get(), [])
    index = find_index(users, user_id)

    if index != -1:
        url = ""
        if is_cover == "True":
            url = users[index]["cover"]
        else:
            url = users[index]["avatar"]
        public_id = os.path.splitext(
            url[url.find(f"FacebookNative/{(folder)}/") : len(url)]
        )[0]
        await delete_media(public_id)

        file_dto = FileDTO(file=file, folder=f"/FacebookNative/{(folder)}")
        result = await upload_media(file_dto)

        content = ContentPost(id=str(uuid.uuid4()), data="", type=1, text="")
        users[index]["bio"] = ""

        post = Post(
            id=str(uuid.uuid4()),
            user=users[index],
            content=content,
            feel="",
            last_time_update=str(datetime.now()),
            time_created=str(datetime.now()),
            tags=[],
            type=(2 if is_cover == "True" else 3),
        )
        posts.append(post.model_dump())

        if is_cover == "True":
            users[index]["cover"] = result["url"]
        else:
            users[index]["avatar"] = result["url"]

        media = Media(
            id=str(uuid.uuid4()), folder=folder, status=1, type=1, url=result["url"]
        )

        ref.child("medias").child("posts").child(post.id).set([media.model_dump()])
        ref.child("users").set(users)
        ref.child("posts").set(posts)
        return {"url": result["url"]}
    return {"url": ""}


async def relationship_check(user1, user2):
    ref = db.reference("social-network")
    relationships = new_value(ref.child("relationships").get(), [])

    if len(relationships) == 0:
        return None
    response = [
        relationship
        for relationship in relationships
        if relationship["user1"] == user1 and relationship["user2"] == user2
    ]
    response = None if len(response) == 0 else response[0]["status"]

    return response


async def get_friend_user(user_id: str):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    relationships = new_value(ref.child("relationships").get(), [])

    if users is None:
        return []

    friends = get_friend_by_id(relationships, users, user_id)

    return [
        {
            "user": user_response(item),
            "manual": get_manual_friend(
                relationships=relationships,
                users=users,
                user1=user_id,
                user2=item["id"],
            ),
        }
        for item in friends
    ]


async def get_request_friend_user(user_id, is_send):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    relationships = new_value(ref.child("relationships").get(), [])

    response = []

    if is_send:
        response = [
            relationship["user2"]
            for relationship in relationships
            if relationship["user1"] == user_id and relationship["status"] == 1
        ]
    else:
        response = [
            relationship["user2"]
            for relationship in relationships
            if relationship["user1"] == user_id and relationship["status"] == 2
        ]

    friends = []
    for item in response:
        index = find_index(users, item)
        if index != -1:
            friends.append(user_response(users[index]))

    return [
        {
            "user": item,
            "manual": get_manual_friend(
                relationships=relationships,
                users=users,
                user1=user_id,
                user2=item["id"],
            ),
        }
        for item in friends
    ]


async def get_friend_main(user_id: str, status: int = 3):
    if status == 3:
        return await get_friend_user(user_id)
    if status == 2:
        return await get_request_friend_user(user_id, False)
    if status == 1:
        return await get_request_friend_user(user_id, True)
    return []
