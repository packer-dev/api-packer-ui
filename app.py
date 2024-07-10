from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import List
import firebase_admin
from firebase_admin import credentials, db
from pydantic import BaseModel
from chatgpt.app import router as chatGPTRouter
from components.app import router as componentRouter
from props.app import router as propRouter
from contents.app import router as contentRouter
from custom.app import router as customRouter
from data.app import router as dataRouter
from messenger.app import router as messengerRouter

app = FastAPI()

cred = credentials.Certificate("./packer-ui-firebase.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://packer-ui-default-rtdb.firebaseio.com/"}
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ComponentDeleteMulti(BaseModel):
    idList: List[str]


@app.post("/components/multi")
async def delete_component(idList: ComponentDeleteMulti):
    try:
        ref = db.reference("/components")
        query = ref.get()
        result = [obj for obj in query if str(obj["id"]) not in idList.idList]
        ref.set(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(chatGPTRouter)
app.include_router(componentRouter)
app.include_router(contentRouter)
app.include_router(propRouter)
app.include_router(customRouter)
app.include_router(dataRouter)
app.include_router(messengerRouter)
