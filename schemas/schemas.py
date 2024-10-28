from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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


class TradeFilter(BaseModel):
    city_id: Optional[int] = None
    product_id: Optional[int] = None
    store_id: Optional[int] = None
    last_n_days: Optional[int] = None
    min_total: Optional[int] = None
    max_total: Optional[int] = None
    min_count: Optional[int] = None
    max_count: Optional[int] = None
