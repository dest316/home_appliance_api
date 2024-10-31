from api.controllers.utils import CRUDableEntity
from schemas.trade import Trade, WriteTrade
from models.models import trades, trades_products, products
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List
from sqlalchemy import select, update, join, insert, delete


# Создание роутера для операций с продажами
router = APIRouter(
    prefix='/api/trade',
    tags=["CRUD_trade"]
)

# Создание объекта Crudable для использования стандарной реализации CRUD-операций
trade = CRUDableEntity(Trade, WriteTrade, trades)


# Метод возвращает продажу из базы данных по id
@router.get("/", response_model=Trade)
async def get_specific_trade(trade_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(trades, products.c.id).select_from(join(trades, trades_products, trades.c.id == trades_products.c.trade_id)
                                        .join(products, trades_products.c.product_id == products.c.id))\
                                        .where(trades.c.id == trade_id)
    result = await session.execute(query)
    row = result.mappings().fetchall()
    if row:
        id_list = [rec["id_1"] for rec in row]
        print(row)
        return Trade(product_id_list=id_list, **row[0])


# Метод возвращает список всех продаж
@router.get("/all", response_model=List[Trade])
async def get_trade(session: AsyncSession = Depends(get_async_session)):
    query = (
        select(
            trades.c.id.label("trade_id"),
            trades.c.date,
            trades.c.store_id,
            products.c.id.label("product_id")
        )
        .select_from(
            join(trades, trades_products, trades.c.id == trades_products.c.trade_id)
            .join(products, products.c.id == trades_products.c.product_id)
        )
    )
    
    # Выполняем запрос и обрабатываем результат
    result = await session.execute(query)
    rows = result.mappings().fetchall()
    
    # Сгруппируем результаты по trade_id и сформируем нужную структуру
    trades_data = {}
    for row in rows:
        trade_id = row["trade_id"]
        if trade_id not in trades_data:
            trades_data[trade_id] = {
                "id": trade_id,
                "date": row["date"],
                "store_id": row["store_id"],
                "product_id_list": []
            }
        trades_data[trade_id]["product_id_list"].append(row["product_id"])
    
    # Преобразуем словарь в список и возвращаем как результат
    return list(map(lambda x: Trade(**x), trades_data.values()))


# Метод для создания новой продажи в базе данных
@router.post("/")
async def add_trade(new_trade: WriteTrade, session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        stmt = insert(trades).values(**new_trade.model_dump(include={"store_id", "date"}))
        result = await session.execute(stmt)
        new_trade_id = result.inserted_primary_key[0]
        trades_products_data = [{"trade_id": new_trade_id, "product_id": product_id} for product_id in new_trade.product_id_list]
        await session.execute(insert(trades_products).values(trades_products_data))
    return {"status": "success"}


# Метод для обновления информации о продаже с указанным id
@router.put("/")
async def update_trade(new_trade: Trade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        stmt = update(trades).where(trades.c.id == new_trade.id)\
        .values(**new_trade.model_dump(include={"store_id", "date", "id"}, exclude_unset=True))
        await session.execute(stmt)
        
        stmt_to_delete = delete(trades_products).where(trades_products.c.trade_id == new_trade.id).execution_options(synchronize_session="fetch")
        await session.execute(stmt_to_delete)
        stmt_to_add = insert(trades_products).values([{"trade_id": new_trade.id, "product_id": prod_id} for prod_id in new_trade.product_id_list])
        await session.execute(stmt_to_add)
    return {"status": "success"}


# Метод для удаления продажи из базы данных по id
@router.delete("/")
async def delete_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        stmt = delete(trades_products).where(trades_products.c.trade_id == trade_id)
        result = await session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail={"message": "Объекта с таким id не существует"})
        stmt = delete(trades).where(trades.c.id == trade_id)
        await session.execute(stmt)
    return {"status": "success"}
