from messenger.models import User, LoginDTO
from firebase_admin import db
from utils import md5, find_index, find_by_id
import uuid


async def getUserById(id: str):
    ref = db.reference("messenger")
    users = ref.child("users").get()

    if users is not None:
        return find_by_id(users, id)
    return None


async def login(loginDTO: LoginDTO):
    ref = db.reference("messenger")
    users = ref.child("users").get()
    if users is not None:
        for obj in users:
            if obj["email"] == loginDTO.email and obj["password"] == md5(
                loginDTO.password
            ):
                return obj
        return None

    return None


def checkExistAccount(user: User, users: list[User]):
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
        checkAccount = checkExistAccount(user, users)
        if checkAccount:
            return {"status": 1, "message": "Email exist in system!"}
        else:
            users.append(user.model_dump())

    ref.child("users").set(users)
    return user


async def updateUserService(user: User):
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


async def getFriends(userId: str):
    ref = db.reference("messenger")
    users = ref.child("users").get()

    if users is None:
        return None

    return [user for user in users if user["id"] != userId]
