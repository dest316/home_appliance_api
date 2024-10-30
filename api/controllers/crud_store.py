from api.controllers.utils import CRUDableEntity
from schemas.store import Store, WriteStore
from models.models import stores
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


# Создание роутера для операций с магазинами
router = APIRouter(
    prefix='/api/store',
    tags=["CRUD_store"]
)

# Создание объекта Crudable для использования стандарной реализации CRUD-операций
store = CRUDableEntity(Store, WriteStore, stores)


# Метод возвращает магазин из базы данных по id
@router.get("/", response_model=Store)
async def get_specific_store(store_id: int, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(store_id, session)
    return result


# Метод возвращает список всех магазинов
@router.get("/all", response_model=List[Store])
async def get_stores(entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


# Метод для создания нового магазина в базе данных
@router.post("/")
async def add_store(new_store: WriteStore, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_store, session)
    return result


# Метод для обновления информации о магазине с указанным id
@router.put("/")
async def update_store(new_store: Store, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_store, session)
    return result


# Метод для удаления магазина из базы данных по id
@router.delete("/")
async def delete_store(store_id: int, entity: CRUDableEntity = Depends(lambda: store), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(store_id, session)
    return result