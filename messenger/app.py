from fastapi import APIRouter, Body
from models import LoginDTO
from services.AuthServices import login, register

router = APIRouter()


@router.post("/api/messenger/v1/login")
async def loginAPI(dto: LoginDTO):
    return login(dto)


@router.post("/api/messenger/v1/register")
async def registerAPI(dto: LoginDTO):
    return register(dto)
