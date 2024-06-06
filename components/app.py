from components.models import Component
from firebase_admin import db
from fastapi import APIRouter, HTTPException
from utils import find_index
router = APIRouter()

def check_component(id: str):
    ref = db.reference("components")
    result = ref.get()
    index = find_index(result, id)
    return {
        "result": result,
        "index": index,
        "ref": ref
    }

@router.post("/components")
async def add_component(component: Component): 
    try:
        ref = db.reference("/components")
        array = ref.get()
        if array is None:
            array = []
        array.append(component.model_dump())
        ref.set(array)
        return component
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/components")
async def get_component(index:int, limit: int): 
    try:
        ref = db.reference("/components")
        query = ref.order_by_key()    
        query = query.start_at(str(index))
        data = query.limit_to_first(limit).get()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/components/getById")
async def get_component_by_id(id: str): 
    try:
        ref = db.reference("/components")
        result = ref.get()
        index = find_index(result, id)
        if (index != -1):
            return result[index]
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/components/count")
async def get_component(): 

    try:
        ref = db.reference("/components")
        result = ref.get()
        return len(result) if result else 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/components/all")
async def get_all_component(): 
    try:
        ref = db.reference("/components")
        result = ref.get()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/components")
async def update_component(component: Component):
    try:
        ref = db.reference("/components")
        result = ref.get()
        index = find_index(result, component.id)
        if (index != -1):
            result[index] = dict(component)
        ref.set(result)
        return component
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))    

@router.delete("/components")
async def delete_component(id:str):
    try:
        ref = db.reference("/components")
        result = ref.get()
        resultFilter = [x for x in result if str(x['id']) != str(id)]
        ref.set(resultFilter)
        return resultFilter
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
