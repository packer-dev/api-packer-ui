import hashlib


def find_index(list, id):
    indexComponent = -1
    for _, item in enumerate(list):
        if str(item["id"]) == str(id):
            return _
    return indexComponent


def md5(password: str) -> str:
    hashed_password = hashlib.md5(password.encode("utf-8"))

    return hashed_password.hexdigest()


def find_by_id(list, id):
    list = [user for user in list if user["id"] == id]
    return None if len(list) == 0 else list[0]
