from pydantic import BaseModel

class WriteCity(BaseModel):
    """Модель pydantic для сущности Город, исключающая id. Подходит для использования в POST-запросах"""
    name: str


class City(WriteCity):
    """Модель pydantic для сущности Город, включающая id. Подходит для использования в GET и PUT-запросах"""
    id: int
    