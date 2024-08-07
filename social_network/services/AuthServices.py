from social_network.models import User, LoginDTO
from firebase_admin import db
from utils import md5, find_index, find_by_id
import uuid


async def get_user_by_id(id: str):
    ref = db.reference("social-network")
    users = ref.child("users").get()

    if users is not None:
        return find_by_id(users, id)
    return None


async def login(login_dto: LoginDTO):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    if users is not None:
        for obj in users:
            if obj["email"] == login_dto.email and obj["password"] == md5(
                login_dto.password
            ):
                return obj
        return None

    return None


def check_exist_account(user: User, users: list[User]):
    for obj in users:
        if obj["email"] == user.email:
            return True

    return False


async def register(user: User):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    user.password = md5(user.password)
    user.id = str(uuid.uuid4())

    if users is None:
        users = [user.model_dump()]
    else:
        check_account = check_exist_account(user, users)
        if check_account:
            return {"status": 1, "message": "Email exist in system!"}
        else:
            users.append(user.model_dump())

    ref.child("users").set(users)
    return user


async def update_user_service(user: User):
    ref = db.reference("social-network")
    users = ref.child("users").get()

    if users is None:
        return None

    index = find_index(users, user.id)
    if index == -1:
        return None

    users[index] = user.model_dump()

    ref.child("users").set(users)
    return users[index]


async def get_friends(user_id: str):
    ref = db.reference("social-network")
    users = ref.child("users").get()
    relationships = ref.child("relationships").get()

    if users is None or relationships is None:
        return []

    relationships = [
        relationship
        for relationship in relationships
        if relationship["user1"] == user_id and relationship["type"] == 3
    ]

    response = []

    for relationship in relationships:
        index = find_index(users, relationship["user2"])
        if index != -1:
            response.append(users[index])

    return response
