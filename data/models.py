from pydantic import BaseModel
from typing import Any

class User(BaseModel):
    id: Any
    name: str
    email: str
    password: str
    avatar: str

class Category(BaseModel):
    id: Any
    name: str
    image: str

class Product(BaseModel):
    id: Any
    name: str
    price: str
    sale: str
    thumbnail: str
    category: Category
