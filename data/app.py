from firebase_admin import db
from fastapi import APIRouter, Body
from data.models import LoginDTO, User, SearchDTO, ProfileDTO
from data.services.AuthService import login, register, getUserById
from data.services.SearchService import searchFilter, searchFilterProduct
from data.services.ProfileService import profileData
from typing import Any

router = APIRouter()


@router.get("/api/data/get")
async def getAll():
    ref = db.reference("data")
    return ref.get()


@router.post("/api/data/set")
async def getAll(data: Any = Body(...)):
    ref = db.reference("data")
    ref.set(data)
    return True


@router.post("/api/categories")
async def getCategories(param: SearchDTO):
    return await searchFilter("categories", param)


@router.post("/api/products")
async def getProducts(param: SearchDTO):
    return await searchFilterProduct(param)


@router.post("/api/users")
async def getUsers(param: SearchDTO):
    return await searchFilter("users", param)


@router.post("/api/auth/login")
async def authLogin(loginDTO: LoginDTO):
    return await login(loginDTO)


@router.post("/api/auth/register")
async def authRegister(user: User):
    return await register(user)


@router.post("/api/profile")
async def profile(param: ProfileDTO):
    return await profileData(param)


@router.get("/api/user/id")
async def getUser(id: str):
    return await getUserById(id)
