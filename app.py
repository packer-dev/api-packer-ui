from fastapi import FastAPI, HTTPException, UploadFile, File
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
from social_network.app import router as socialNetworkRouter

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


app.include_router(chatGPTRouter)
app.include_router(componentRouter)
app.include_router(contentRouter)
app.include_router(propRouter)
app.include_router(customRouter)
app.include_router(dataRouter)
app.include_router(socialNetworkRouter)
