from fastapi import APIRouter
from data.models import LoginDTO, User, SearchDTO, ProfileDTO
from data.services.AuthService import login, register
from data.services.SearchService import searchFilter
from data.services.ProfileService import profileData

router = APIRouter()


@router.post("/api/categories")
async def getCategories(param: SearchDTO):
    return await searchFilter("categories", param)


@router.post("/api/products")
async def getProducts(param: SearchDTO):
    return await searchFilter("products", param)


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
