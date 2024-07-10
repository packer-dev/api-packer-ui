from fastapi import APIRouter, Body
from messenger.models import LoginDTO
from messenger.services.AuthServices import login, register

router = APIRouter()


@router.post("/api/messenger/v1/login")
async def loginAPI(dto: LoginDTO):
    return login(dto)


@router.post("/api/messenger/v1/register")
async def registerAPI(dto: LoginDTO):
    return register(dto)
