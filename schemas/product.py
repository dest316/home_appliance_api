from pydantic import BaseModel


class WriteProduct(BaseModel):
    """Модель pydantic для сущности Товар, исключающая id. Подходит для использования в POST-запросах"""
    name: str
    price: int


class Product(WriteProduct):
    """Модель pydantic для сущности Товар, включающая id. Подходит для использования в GET и PUT-запросах"""
    id: int
