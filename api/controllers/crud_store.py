from api.controllers.utils import CRUDableEntity
from schemas.store import Store, WriteStore
from models.models import stores
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


router = APIRouter(
    prefix='/api/store',
    tags=["CRUD_store"]
)

store = CRUDableEntity(Store, WriteStore, stores)

@router.get("/", response_model=Store)
async def get_specific_store(store_id: int, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(store_id, session)
    return result


@router.get("/all", response_model=List[Store])
async def get_stores(entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/")
async def add_trade(new_store: Store, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_store, session)
    return result

@router.put("/")
async def update_store(new_store: Store, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_store, session)
    return result

@router.delete("/")
async def delete_store(store_id: int, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(store_id, session)
    return result