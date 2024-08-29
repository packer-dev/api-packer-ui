from firebase_admin import db
from utils import new_value, find_index
from social_network.models import Notification
import uuid
from datetime import datetime


async def get_notification_by_user(user_id: str, limit: int = 10, offset: int = 0):
    ref = db.reference("social-network")
    notifications = new_value(ref.child("notifications").child(user_id).get(), [])
    notifications = sorted(
        notifications, key=lambda x: x["last_update_time"], reverse=True
    )
    return {
        "list": notifications[offset : limit * (1 if offset == 0 else offset)],
        "total": len(notifications),
    }


async def mark_read_notification(user_id: str):
    ref = db.reference("social-network")
    notifications = new_value(ref.child("notifications").child(user_id).get(), [])
    for index, item in enumerate(notifications):
        notifications[index]["is_read"] = True
    ref.child("notifications").child(user_id).set(notifications)

    return True


async def add_notification(notification: Notification, type: int):
    ref = db.reference("social-network")
    notifications = new_value(
        ref.child("notifications").child(notification.user.id).get(), []
    )

    if type == 1:
        index = -1
        for pos, item in enumerate(notifications):
            if item["main_id"] == notification.main_id:
                index = pos
                break
        if index != -1:
            notification = notifications[index]
            notification["last_update_time"] = str(datetime.now())
    else:
        notification.id = str(uuid.uuid4())
        notification.time_created = str(datetime.now())
        notification.last_update_time = str(datetime.now())
        notifications = [notification.model_dump()] + notifications
    ref.child("notifications").child(notification.user.id).set(notifications)

    return notification
