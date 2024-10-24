from pydantic import BaseModel
from datetime import datetime


class City(BaseModel):
    id: int
    name: str


class Store(BaseModel):
    id: int
    city_id: int
    address: str


class Trade(BaseModel):
    id: int
    store_id: int
    date: datetime


class Product(BaseModel):
    id: int
    name: str
    price: int