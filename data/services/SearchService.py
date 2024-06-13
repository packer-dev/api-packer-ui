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


async def searchFilterProduct(param: SearchDTO):
    ref = db.reference("data")
    data = ref.get()
    param = param.model_dump()

    limit = param["limit"]
    offset = param["offset"]
    search = param["search"]
    filters = param["filters"]

    if data is None:
        return {"list": [], "total": 0}
    list = data["products"] if "products" in data else []
    if "category" in filters:
        list = [
            product
            for product in list
            if product["category"]["id"] == filters["category"]
        ]
    if search != "":
        list = [
            product
            for product in list
            if str(search).lower() in str(product["name"]).lower()
        ]
    return {
        "list": (list if limit == 0 else list[offset:limit]),
        "total": len(list),
    }
