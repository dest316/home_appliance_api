from fastapi import APIRouter, Depends, HTTPException
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, Table
from models.models import cities, trades, products, stores
from typing import List, Dict
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

    async def get(self, target_id, session: AsyncSession) -> BaseModel:
        query = select(self.target_table).where(self.target_table.c.id == target_id)
        result = await session.execute(query)
        row = result.mappings().fetchone()
        if row:
            return self.read_model(**row)
    
    async def get_all(self, session: AsyncSession) -> List[BaseModel]:
        query = select(self.target_table)
        result = await session.execute(query)
        return list(result.mappings())
    
    async def post(self, new_entity: BaseModel, session: AsyncSession) -> Dict:
        stmt = insert(self.target_table).values(**new_entity.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    
    async def put(self, new_entity: BaseModel, session: AsyncSession, exclude_unset: bool = False) -> Dict:
        stmt = update(self.target_table).where(self.target_table.c.id == new_entity.id).values(**new_entity.model_dump(exclude_unset=exclude_unset)).execution_options(synchronize_session="fetch")
        result = await session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail={"message": "Объекта с таким id не существует"})
        await session.commit()
        return {"status": "success"}
    
    async def delete(self, target_id: int, session: AsyncSession) -> Dict:
        stmt = delete(self.target_table).where(self.target_table.c.id == target_id)
        result = await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    
    async def patch(self, patched_entity: BaseModel, session: AsyncSession):
        return await self.put(patched_entity, session, exclude_unset=True)
    

trade = CRUDableEntity(Trade, None, trades)
city = CRUDableEntity(City, None, cities)
store = CRUDableEntity(Store, None, stores)
product = CRUDableEntity(Product, None, products)


router = APIRouter(
    prefix='/api',
    tags=["CRUD_operations"]
)

@router.get("/city", response_model=City)
async def get_specific_city(city_id: int, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(city_id, session)
    return result


@router.get("/cities", response_model=List[City])
async def get_cities(entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/city")
async def add_city(new_city: City, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_city, session)
    return result

@router.put("/city")
async def update_city(new_city: City, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_city, session)
    return result

@router.delete("/city")
async def delete_city(city_id: int, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(city_id, session)
    return result

@router.patch("/city")
async def patch_city(patched_city: City, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.patch(patched_city, session)
    return result


@router.get("/product", response_model=Product)
async def get_specific_product(product_id: int, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(product_id, session)
    return result


@router.get("/products", response_model=List[Product])
async def get_products(entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/product")
async def add_product(new_product: Product, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_product, session)
    return result

@router.put("/product")
async def update_product(new_product: Product, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_product, session)
    return result

@router.delete("/product")
async def delete_product(product_id: int, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(product_id, session)
    return result


@router.get("/store", response_model=Store)
async def get_specific_store(store_id: int, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(store_id, session)
    return result


@router.get("/stores", response_model=List[Store])
async def get_stores(entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/store")
async def add_trade(new_store: Store, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_store, session)
    return result

@router.put("/store")
async def update_store(new_store: Store, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_store, session)
    return result

@router.delete("/store")
async def delete_store(store_id: int, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(store_id, session)
    return result


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
