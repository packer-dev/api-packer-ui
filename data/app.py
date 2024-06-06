from firebase_admin import db
from fastapi import APIRouter
from data.models import LoginDTO, User

router = APIRouter()


async def searchLimit(path: str,offset: int, limit: int):
    ref = db.reference("data")
    data = ref.get()
    if (data is None): return {
        'list': [],
        'total': 0
    }
    list = data[path] if path in data else []
    return {
        'list': list if limit == 0 else list[offset:limit],
        'total': len(list)
    }

@router.get("/api/categories")
async def getCategories(offset: int, limit: int):
    return await searchLimit("categories",offset, limit)

@router.get("/api/products")
async def getProducts(offset: int, limit: int):
    return await searchLimit("products",offset, limit)

@router.get("/api/users")
async def getUsers(offset: int, limit: int):
    return await searchLimit("users",offset, limit)

@router.post("/api/auth/login")
async def getUsers(loginDTO: LoginDTO):
    ref = db.reference("data")
    data = ref.get()
    if (data is None or 'users' not in data): 
        return {
            'status': 1,
            'message': 'Email or password incorrect!'
        }
    else:
        data = data['users']
        for obj in data:
            if obj['email'] == loginDTO.email and obj['password'] == loginDTO.password:
                return obj
        return {
            'status': 1,
            'message': 'Email or password incorrect!'
        }

def checkExistAccount(user: User, users: list[User]):
    for obj in users:
        if obj['email'] == user.email:
            return True 
    return False

@router.post("/api/auth/register")
async def getUsers(user: User):
    ref = db.reference("data")
    data = ref.get()

    if (data is None): 
        ref.set({
            'users': [dict(user)]
        })
        return user
    else:
        if ('users' not in data):
            data['users'] = [dict(user)]
        else:
            checkAccount = checkExistAccount(user, data['users'])
            if (checkAccount):
                return {
                    'status': 1,
                    'message': 'Email exist in system!'
                }
            else:
                data['users'].append(dict(user))
        
        ref.set(data)
        return user
       
        