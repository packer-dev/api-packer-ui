from messenger.models import User, LoginDTO
from firebase_admin import db
from utils import md5, find_index, find_by_id
import uuid


async def get_user_by_id(id: str):
    ref = db.reference("messenger")
    users = ref.child("users").get()

    if users is not None:
        return find_by_id(users, id)
    return None


async def login(login_dto: LoginDTO):
    ref = db.reference("messenger")
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
    ref = db.reference("messenger")
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
    ref = db.reference("messenger")
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
    ref = db.reference("messenger")
    users = ref.child("users").get()

    if users is None:
        return None

    return [user for user in users if user["id"] != user_id]
