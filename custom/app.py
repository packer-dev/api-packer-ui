from firebase_admin import db
from fastapi import APIRouter, HTTPException
from utils import find_index
from pydantic import BaseModel
router = APIRouter()
from typing import Any
from collections import OrderedDict

class RequestDTO(BaseModel):
    path:str
    object: Any

class SearchLimit(BaseModel):
    limit: int
    offset: int
    search: str = ""
    filters: Any

class SearchLimitDTO(BaseModel):
    path: str
    object: SearchLimit

@router.post("/custom")
async def add_custom(request: RequestDTO): 
    try:
        data = request.model_dump();
        ref = db.reference("/" + data['path'])
        array = ref.get()
        if array is None:
            array = []
        array.append(request['object'])
        ref.set(array)
        return request['object']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/custom/search")
async def get_custom(searchLimit: SearchLimitDTO): 
    try:
        params = searchLimit.model_dump()
        ref = db.reference("/" + params['path'])
        # array = ref.get()
        # if array is None:
        #     array = []
        query = ref.order_by_key()    
        query = query.start_at(str(params['object']['offset']))
        data = query.limit_to_first(params['object']['limit']).get()
        response = {}
        data = [] if data is None else list(data.values()) if isinstance(data, OrderedDict) else data
        response['list'] = [item for item in data if item is not None]
        response['total'] = len([] if ref.get() is None else ref.get())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/custom")
async def update_component(request: RequestDTO):
    try:
        ref = db.reference("/" + request.path)
        result = ref.get()
        index = find_index(result, request.object.id)
        if (index != -1):
            result[index] = dict(request.object)
        ref.set(result)
        return request.object
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))    

@router.delete("/components")
async def delete_component(id:str, path: str):
    try:
        ref = db.reference("/" + path)
        result = ref.get()
        resultFilter = [x for x in result if str(x['id']) != str(id)]
        ref.set(resultFilter)
        return resultFilter
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



