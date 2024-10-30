from pydantic import BaseModel


class WriteStore(BaseModel):
    """Модель pydantic для сущности Магазин, исключающая id. Подходит для использования в POST-запросах"""
    city_id: int
    address: str


class Store(WriteStore):
    """Модель pydantic для сущности Магазин, включающая id. Подходит для использования в GET и PUT-запросах"""
    id: int
