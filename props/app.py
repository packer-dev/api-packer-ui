from firebase_admin import db
from fastapi import APIRouter
from props.models import Prop
from utils import find_index

router = APIRouter()

@router.get("/components/props")
async def get_props_by_id_component(id: str):
    ref = db.reference("components")
    components = ref.get()
    index = find_index(components, id)
    if (index == -1):
        return []
    else:
        props = components[index]['props'] if 'props' in components[index] and components[index]['props'] is not None else []
        return props
    
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
