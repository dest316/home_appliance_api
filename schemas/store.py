from pydantic import BaseModel


class WriteStore(BaseModel):
    city_id: int
    address: str


class Store(WriteStore):
    id: int
