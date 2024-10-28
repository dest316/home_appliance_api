from pydantic import BaseModel


class WriteProduct(BaseModel):
    name: str
    price: int


class Product(WriteProduct):
    id: int
