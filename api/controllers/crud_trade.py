from api.controllers.utils import CRUDableEntity
from schemas.trade import Trade, WriteTrade
from models.models import trades
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


# Создание роутера для операций с продажами
router = APIRouter(
    prefix='/api/trade',
    tags=["CRUD_trade"]
)

# Создание объекта Crudable для использования стандарной реализации CRUD-операций
trade = CRUDableEntity(Trade, WriteTrade, trades)


# Метод возвращает продажу из базы данных по id
@router.get("/", response_model=Trade)
async def get_specific_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(trade_id, session)
    return result


# Метод возвращает список всех продаж
@router.get("/all", response_model=List[Trade])
async def get_trade(entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


# Метод для создания новой продажи в базе данных
@router.post("/")
async def add_trade(new_trade: WriteTrade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_trade, session)
    return result


# Метод для обновления информации о продаже с указанным id
@router.put("/")
async def update_trade(new_trade: Trade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_trade, session)
    return result


# Метод для удаления продажи из базы данных по id
@router.delete("/")
async def delete_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(trade_id, session)
    return result
