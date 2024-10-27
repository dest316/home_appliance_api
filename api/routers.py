from fastapi import APIRouter, Depends, HTTPException
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, Table
from models.models import cities, trades, products, stores
from typing import List
from schemas.schemas import City, Trade, Store, Product
from pydantic import BaseModel


class CRUDableEntity:
    read_model: BaseModel
    write_model: BaseModel
    target_table: Table

    def __init__(self, read_model, write_model, target_table) -> None:
        self.read_model = read_model
        self.write_model = write_model
        self.target_table = target_table

    async def get(self, target_id, session: AsyncSession):
        query = select(self.target_table).where(self.target_table.c.id == target_id)
        result = await session.execute(query)
        row = result.mappings().fetchone()
        if row:
            return self.read_model(**row)
    
    async def get_all(self, session: AsyncSession):
        query = select(self.target_table)
        result = await session.execute(query)
        return list(result.mappings())
    
    async def post(self, new_entity: BaseModel, session: AsyncSession):
        stmt = insert(self.target_table).values(**new_entity.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    
    async def put(self, new_entity: BaseModel, session: AsyncSession):
        stmt = update(self.target_table).where(self.target_table.c.id == new_entity.id).values(**new_entity.model_dump(exclude_unset=False)).execution_options(synchronize_session="fetch")
        result = await session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail={"message": "Объекта с таким id не существует"})
        await session.commit()
        return {"status": "success"}
    
    async def delete(self, target_id: int, session: AsyncSession):
        stmt = delete(self.target_table).where(self.target_table.c.id == target_id)
        result = await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    
    async def patch(self, target_id: int, session: AsyncSession):
        pass
    

trade = CRUDableEntity(Trade, None, trades)


router = APIRouter(
    prefix='/api',
    tags=["CRUD_operations"]
)

@router.get("/cities")
async def get_city(session: AsyncSession = Depends(get_async_session)):
    query = select(cities)
    result = await session.execute(query)
    return list(result.mappings())


@router.get("/city")
async def get_specific_city(city_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(cities).where(cities.c.id == city_id)
    result = await session.execute(query)
    return result.mappings().fetchone()


# To-do: Добавить проверку на уникальность id, по-хорошему сделать уникальным так же и название города, и не добавлять id в запросе
# т.к. он автоматически генерируется в бд
@router.post("/city")
async def add_city(new_city: City, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(cities).values(**new_city.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/city")
async def replace_city(new_city: City, session: AsyncSession = Depends(get_async_session)):
    stmt = update(cities).where(cities.c.id == new_city.id).values(**new_city.model_dump(exclude_unset=False)).execution_options(synchronize_session="fetch")
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail={"message": "Города с таким id не существует"})
    await session.commit()
    return {"status": "success"}


@router.delete("/city")
async def delete_city(deleted_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(cities).where(cities.c.id == deleted_id)
    result = await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/products")
async def get_product(session: AsyncSession = Depends(get_async_session)):
    query = select(products)
    result = await session.execute(query)
    return list(result.mappings())


@router.get("/product")
async def get_specific_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(products).where(products.c.id == product_id)
    result = await session.execute(query)
    return result.mappings().fetchone()


@router.post("/product")
async def add_product(new_product: Product, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(products).values(**new_product.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"result": "success"}


@router.put("/product")
async def update_product(new_product: Product, session: AsyncSession = Depends(get_async_session)):
    stmt = update(products).where(products.c.id == new_product.id).values(**new_product.model_dump(exclude_unset=False)).execution_options(synchronize_session="fetch")
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail={"message": "Товара с таким id не существует"})
    await session.commit()
    return {"status": "success"}


@router.delete("/product")
async def delete_product(deleted_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(products).where(products.c.id == deleted_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/stores")
async def get_stores(session: AsyncSession = Depends(get_async_session)):
    query = select(stores)
    result = await session.execute(query)
    return list(result.mappings())


@router.get("/store")
async def get_specific_store(store_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(stores).where(stores.c.id == store_id)
    result = await session.execute(query)
    return result.mappings().fetchone()


@router.post("/store")
async def add_store(new_store: Store, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(products).values(**new_store.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"result": "success"}


@router.put("/store")
async def update_store(new_store: Store, session: AsyncSession = Depends(get_async_session)):
    stmt = update(stores).where(stores.c.id == new_store.id).values(**new_store.model_dump(exclude_unset=False)).execution_options(synchronize_session="fetch")
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail={"message": "Продукта с таким id не существует"})
    await session.commit()
    return {"status": "success"}


@router.delete("/store")
async def delete_store(store_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(stores).where(stores.c.id == store_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/trade", response_model=Trade)
async def get_specific_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(trade_id, session)
    return result


@router.get("/trades", response_model=List[Trade])
async def get_trade(entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/trade")
async def add_trade(new_trade: Trade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_trade, session)
    return result

@router.put("/trade")
async def update_trade(new_trade: Trade, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_trade, session)
    return result

@router.delete("/trade")
async def delete_trade(trade_id: int, entity: CRUDableEntity = Depends(lambda: trade), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(trade_id, session)
    return result
