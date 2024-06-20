from data.models import User, LoginDTO, PasswordPTO
from firebase_admin import db
from utils import md5, find_index
import uuid


async def getUserById(id: str):
    ref = db.reference("data")
    data = ref.get()

    users = [] if "users" not in data else data["users"]
    users = [user for user in users if user["id"] == id]
    return None if len(users) == 0 else users[0]


async def login(loginDTO: LoginDTO):
    ref = db.reference("data")
    data = ref.get()
    if data is None or "users" not in data:
        return {"status": 1, "message": "Email or password incorrect!"}
    else:
        data = data["users"]
        for obj in data:
            if obj["email"] == loginDTO.email and obj["password"] == md5(
                loginDTO.password
            ):
                return obj
        return {"status": 1, "message": "Email or password incorrect!"}


def checkExistAccount(user: User, users: list[User]):
    for obj in users:
        if obj["email"] == user.email:
            return True
    return False


async def register(user: User):
    ref = db.reference("data")
    data = ref.get()
    user.password = md5(user.password)
    user.id = str(uuid.uuid4())
    if data is None:
        ref.set({"users": [user.model_dump()]})
        return user
    else:
        if "users" not in data:
            data["users"] = [user.model_dump()]
        else:
            checkAccount = checkExistAccount(user, data["users"])
            if checkAccount:
                return {"status": 1, "message": "Email exist in system!"}
            else:
                data["users"].append(user.model_dump())
        ref.set(data)
        return user


async def updateUserService(user: User):
    ref = db.reference("data")
    data = ref.get()
    users = data["users"]
    index = find_index(users, user.id)
    if index == -1:
        return None
    users[index] = user.model_dump()
    data["users"] = users
    ref.set(data)
    return users[index]


async def changePassword(passwordDTO: PasswordPTO):
    passwordDTO = passwordDTO.model_dump()
    ref = db.reference("data")
    data = ref.get()

    index = find_index(data["users"], passwordDTO["id"])
    if index == -1:
        return False
    else:
        data["users"][index]["password"] = md5(passwordDTO["password"])
        ref.set(data)
        return True
