from firebase_admin import db
from fastapi import APIRouter
from props.models import Prop
from utils import find_index

router = APIRouter()


async def searchLimit(path: str,offset: int, limit: int):
    ref = db.reference("data")
    data = ref.get()
    if (data is None): return {
        'list': [],
        'total': 0
    }
    list = data[path] if path in data else []
    return {
        'list': list if limit == 0 else list[offset:limit],
        'total': len(list)
    }

@router.get("/api/categories")
async def getCategories(offset: int, limit: int):
    return await searchLimit("categories",offset, limit)

@router.get("/api/products")
async def getProducts(offset: int, limit: int):
    return await searchLimit("products",offset, limit)

@router.get("/api/users")
async def getUsers(offset: int, limit: int):
    return await searchLimit("users",offset, limit)

    
@router.post("/components/props")
async def get_props_by_id_component(prop: Prop, id: str):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, id)
    if (index == -1):
        return []
    else:
        if 'props' in components[index] and components[index]['props'] is not None:
            props = components[index]['props']
            props.append(prop.model_dump()) 
            components[index]['props'] = props
        else:
            components[index]['props'] = [prop.model_dump()]

        ref.set(components)
        return dict(prop)

@router.delete("/components/props")
async def get_props_by_id_component(idProp: str, idComponent: str):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, idComponent)
    if (index == -1):
        return []
    else:
        if 'props' in components[index] and components[index]['props'] is not None:
            props = components[index]['props']
            props = [x for x in props if str(x['id']) != str(idProp)]
            components[index]['props'] = props

            ref.set(components)
        return True

@router.put("/components/props")
async def update_props_by_id_component(prop: Prop, id: str):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, id)
    if (index == -1):
        return []
    else:
        if 'props' in components[index] and components[index]['props'] is not None:
            props = components[index]['props']
            indexProp = find_index(props, prop.id)
            props[indexProp] = prop.model_dump()
            components[index]['props'] = props

            ref.set(components)
        return True
