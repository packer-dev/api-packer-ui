from firebase_admin import db
from utils import find_index
import uuid


async def test():
    ref = db.reference("social-network")
    ref.child("messages").child("abc").set({"a": 1})
    return ref.child("messages").get()


async def check_role_view_profile(user1: str, user2: str):
    ref = db.reference("social-network")
    relationships = ref.child("relationships").get()

    if relationships is None:
        return None

    relationships = [
        relationship
        for relationship in relationships
        if relationship["user1"] == user1 and relationship["user2"] == user2
    ]

    return None if len(relationships) == 0 else relationships[0]
