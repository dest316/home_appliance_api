from api.controllers.utils import CRUDableEntity
from schemas.trade import Trade, WriteTrade
from models.models import trades
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


router = APIRouter(
    prefix='/api/trade',
    tags=["CRUD_trade"]
)

trade = CRUDableEntity(Trade, WriteTrade, trades)

@router.get("/", response_model=Trade)
async def get_specific_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(trade_id, session)
    return result


@router.get("/all", response_model=List[Trade])
async def get_trade(entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/")
async def add_trade(new_trade: Trade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_trade, session)
    return result

@router.put("/")
async def update_trade(new_trade: Trade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_trade, session)
    return result

@router.delete("/")
async def delete_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(trade_id, session)
    return result
