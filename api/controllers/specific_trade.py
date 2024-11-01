from fastapi import Depends, APIRouter
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join, and_, func
from models.models import trades, products, stores, trades_products
from schemas.trade import TradeFilter
from datetime import datetime, timedelta
from typing import List, Dict


# Создание роутера для нестандартных операций с продажами
router = APIRouter(
    prefix='/api/spec_trade',
    tags=["Spec_trade"]
)


# Метод для получения отфильтрованных продаж по различным критериям. В случае, если ни один критерий не указан, возвращает список из всех продаж
@router.get("/get_filtered_trades")
async def get_filtered_trades(filters: TradeFilter = Depends(), session: AsyncSession = Depends(get_async_session)) -> List[Dict]:
    conditions = []

    # Заполняем список условий SQL-запроса, в зависимости от переданных в запрос параметров 
    if filters.city_id is not None:
        conditions.append(stores.c.city_id == filters.city_id)
    if filters.product_id is not None:
        conditions.append(trades_products.c.product_id == filters.product_id)
    if filters.store_id is not None:
        conditions.append(trades.c.store_id == filters.store_id)
    if filters.last_n_days is not None:
        last_date = datetime.now() - timedelta(days=filters.last_n_days)
        conditions.append(trades.c.date >= last_date)

    # Формируем запрос к базе данных
    query = select(trades,
                   func.sum(products.c.price).label("total_price"),
                    func.count(products.c.id).label("total_count"))\
                        .select_from(join(trades, trades_products, trades.c.id == trades_products.c.trade_id)
                                       .join(products, products.c.id == trades_products.c.product_id)
                                       .join(stores, trades.c.store_id == stores.c.id)).where(
                                           and_(
                                               *conditions
                                           )
                                       ).group_by(
                                           trades.c.id
                                       )
    
    # Дополняем запрос с помощью having для обработки условий, связанных с агрегатными функциями SQL
    if filters.min_total is not None:
        query = query.having(func.sum(products.c.price) > filters.min_total)
    if filters.max_total is not None:
        query = query.having(func.sum(products.c.price) < filters.max_total)
    if filters.min_count is not None:
        query = query.having(func.count(products.c.id) > filters.min_count)
    if filters.max_count is not None:
        query = query.having(func.count(products.c.id) < filters.max_count)

    # Выполняем сформированный запрос, получаем результат и возвращаем его в виде списка
    result = await session.execute(query)
    return list(result.mappings())
