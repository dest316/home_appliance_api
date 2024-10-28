from pydantic import BaseModel


class WriteCity(BaseModel):
    name: str


class City(WriteCity):
    id: int
    