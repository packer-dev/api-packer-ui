def post_response(post: dict) -> dict:
    return {
        "id": post.get("id"),
        "user": user_response(post.get("user")),
        "content": post.get("content"),
        "time_created": post.get("time_created"),
        "last_time_update": post.get("last_time_update"),
        "type": post.get("type"),
        "tags": post.get("tags"),
        "feel": post.get("feel"),
    }


def user_response(user: dict) -> dict:

    return (
        None
        if user is None
        else {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "avatar": user.get("avatar"),
            "cover": user.get("cover"),
            "last_time_active": user.get("last_time_active"),
            "time_created": user.get("time_created"),
            "bio": user.get("bio"),
        }
    )


def member_response(member: dict) -> dict:
    return {
        "id": member.get("id"),
        "nickname": member.get("nickname"),
        "user": user_response(member.get("user")),
        "is_owner": member.get("is_owner"),
    }


def group_response(group: dict) -> dict:
    return {
        "id": group.get("id"),
        "name": group.get("name"),
        "members": [member_response(member) for member in group.get("members", [])],
        "last_message": message_response(
            group.get("last_message")
        ),  # Assuming last_message is already in dict format
        "data": group.get("data"),  # Assuming data is already in dict format
        "time_created": group.get("time_created"),
        "last_time_update": group.get("last_time_update"),
        "image": group.get("image"),
        "seen": group.get("seen"),
        "multiple": group.get("multiple"),
    }


def message_response(message: dict) -> dict:
    return (
        None
        if message is None
        else {
            "id": message.get("id"),
            "content": message.get(
                "content"
            ),  # Assuming content is already in dict format
            "user": message.get("user"),  # Assuming user is already in dict format
            "time_created": message.get("time_created"),
        }
    )
