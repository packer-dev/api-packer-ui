from fastapi import APIRouter
from messenger.models import LoginDTO, User, SendMessageDTO, Group
from messenger.services.AuthServices import login, register, getUserById
from messenger.services.MessageService import sendMessage, getGroupByUser, updateGroup

router = APIRouter()


@router.post("/api/messenger/v1/login")
async def loginAPI(dto: LoginDTO):
    return await login(dto)


@router.post("/api/messenger/v1/register")
async def registerAPI(dto: User):
    return await register(dto)


@router.get("/api/messenger/v1/user/id")
async def getUserByIdAPI(userId: str):
    return await getUserById(userId)


@router.get("/api/messenger/v1/message/send")
async def sendMessageAPI(dto: SendMessageDTO):
    return await sendMessage(dto)


@router.get("/api/messenger/v1/message/list")
async def getGroupByUserAPI(userId: str):
    return await getGroupByUser(userId)


@router.get("/api/messenger/v1/group/update")
async def updateGroupAPI(group: Group):
    return await updateGroup(group)
