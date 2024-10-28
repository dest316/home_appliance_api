from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WriteTrade(BaseModel):
    store_id: int
    date: datetime


class Trade(BaseModel):
    id: int
    

class TradeFilter(BaseModel):
    city_id: Optional[int] = None
    product_id: Optional[int] = None
    store_id: Optional[int] = None
    last_n_days: Optional[int] = None
    min_total: Optional[int] = None
    max_total: Optional[int] = None
    min_count: Optional[int] = None
    max_count: Optional[int] = None
