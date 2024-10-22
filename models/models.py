from pydantic import BaseModel, constr
from datetime import datetime
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column


# class City(BaseModel):
#     id: int
#     name: str


# class Store(BaseModel):
#     id: int
#     city_id: int
#     address: str


# class Trade(BaseModel):
#     id: int
#     store_id: int
#     date: datetime


# class Product(BaseModel):
#     id: int
#     name: str
#     price: int


metadata = MetaData()

cities = Table(
    "cities",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False)
)

stores = Table(
    "stores",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("address", String, nullable=False),
    Column("city_id", Integer, ForeignKey("cities.id"))
)

trades = Table(
    "trades",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", TIMESTAMP, nullable=False),
    Column("store_id", Integer, ForeignKey("stores.id"))
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("price", Integer, nullable=False)
)

trades_products = Table(
    "trades_products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("trade_id", Integer, ForeignKey("trades.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)
