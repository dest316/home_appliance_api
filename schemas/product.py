from pydantic import BaseModel, Field


class WriteProduct(BaseModel):
    """Модель pydantic для сущности Товар, исключающая id. Подходит для использования в POST-запросах"""
    name: str
    price: int = Field(ge=1)


class Product(WriteProduct):
    """Модель pydantic для сущности Товар, включающая id. Подходит для использования в GET и PUT-запросах"""
    id: int
