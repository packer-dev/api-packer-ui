from data.models import User, LoginDTO
from firebase_admin import db
from utils import md5
import uuid


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


async def checkExistAccount(user: User, users: list[User]):
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
        ref.set({"users": [dict(user)]})
        return user
    else:
        if "users" not in data:
            data["users"] = [dict(user)]
        else:
            checkAccount = checkExistAccount(user, data["users"])
            if checkAccount:
                return {"status": 1, "message": "Email exist in system!"}
            else:
                data["users"].append(dict(user))
        ref.set(data)
        return user
