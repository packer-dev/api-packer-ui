from firebase_admin import db
from utils import new_value


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


async def get_navbar_amount_new(user_id: str):
    ref = db.reference("social-network")
    notifications = new_value(ref.child("notifications").child(user_id).get(), [])
    notifications = [item for item in notifications if item["is_read"] == False]
    return {
        "friend": 0,
        "notification": len(notifications),
        "watch": 0,
        "marketplace": 0,
    }
