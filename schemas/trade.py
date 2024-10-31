from pydantic import BaseModel, conlist
from datetime import datetime
from typing import Optional, List


class WriteTrade(BaseModel):
    """Модель pydantic для сущности Продажа, исключающая id. Подходит для использования в POST-запросах"""
    store_id: int
    date: datetime
    product_id_list: conlist(int, min_length=1) # type: ignore


class Trade(WriteTrade):
    """Модель pydantic для сущности Магазин, включающая id. Подходит для использования в GET и PUT-запросах"""
    id: int
    

class TradeFilter(BaseModel):
    """Модель pydantic для параметров сортировки продаж"""
    city_id: Optional[int] = None
    product_id: Optional[int] = None
    store_id: Optional[int] = None
    last_n_days: Optional[int] = None
    min_total: Optional[int] = None
    max_total: Optional[int] = None
    min_count: Optional[int] = None
    max_count: Optional[int] = None
