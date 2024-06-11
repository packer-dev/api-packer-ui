from firebase_admin import db
from data.models import SearchDTO


async def searchFilter(path: str, param: SearchDTO):
    ref = db.reference("data")
    data = ref.get()

    if data is None:
        return {"list": [], "total": 0}
    list = data[path] if path in data else []
    return {
        "list": (list if param.limit == 0 else list[param.offset : param.limit]),
        "total": len(list),
    }
