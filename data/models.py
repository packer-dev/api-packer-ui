from pydantic import BaseModel
from typing import Any, List


class SearchDTO(BaseModel):
    limit: int
    offset: int
    search: str
    filters: Any


class LoginDTO(BaseModel):
    email: str
    password: str


class Address(BaseModel):
    id: str
    fullname: str
    address: str
    city: str
    province: str
    zip_code: str
    country: str
    phone: str


class Bank(BaseModel):
    id: str


class Category(BaseModel):
    id: str
    name: str
    image: str


class Product(BaseModel):
    id: str
    name: str
    price: int
    sale: int
    image: str
    category: Category


class DetailOrder(BaseModel):
    id: str
    product: Product
    amount: int


class Order(BaseModel):
    id: str
    address: Address
    prom_code: str
    details: List[DetailOrder]
    time_created: str


class PromCode(BaseModel):
    id: str
    name: str
    code: str
    expired_date: str


class Bag(BaseModel):
    id: str
    product: Product
    amount: int


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    avatar: str
    addresses: List[Address]
    banks: List[Bank]
    orders: List[Order]
    prom_codes: List[PromCode]
    bags: List[Bag]
    favorites: List[Product]


class ProfileDTO(BaseModel):
    type: str
    data: Any
    user: User
    isDelete: bool
