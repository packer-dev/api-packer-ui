from pydantic import BaseModel
from typing import Any
from models import Category

class Product(BaseModel):
    id: Any
    name: str
    status: bool
    price: int
    sale: int
    categoryProduct: Category
    timeCreated: str
    lastModifiedTime: str