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
    price: float
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


class Favorite(BaseModel):
    id: str
    product: Product


class Notification(BaseModel):
    sales: bool
    new_arrivals: bool
    delivery_status: bool


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    avatar: str
    addresses: List[str]
    banks: List[str]
    orders: List[str]
    prom_codes: List[str]
    bags: List[str]
    favorites: List[str]
    birthday: str
    settings: Notification


class ProfileDTO(BaseModel):
    type: str
    data: Any
    user: User
    isDelete: bool


class GetProfileDTO(BaseModel):
    type: str
    idUser: str
    idProfile: str


class PasswordPTO(BaseModel):
    id: str
    password: str
