from api.controllers.utils import CRUDableEntity
from schemas.city import City, WriteCity
from models.models import cities
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


# Создание роутера для операций с городами
router = APIRouter(
    prefix='/api/city',
    tags=["CRUD_city"]
)

# Создание объекта Crudable для использования стандарной реализации CRUD-операций
city = CRUDableEntity(City, WriteCity, cities)


# Метод возвращает город из базы данных по id
@router.get("/", response_model=City)
async def get_specific_city(city_id: int, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(city_id, session)
    return result


# Метод возвращает список всех городов
@router.get("/all", response_model=List[City])
async def get_cities(entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


# Метод для создания нового города в базе данных
@router.post("/")
async def add_city(new_city: WriteCity, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_city, session)
    return result


# Метод для обновления информации о городе с указанным id
@router.put("/")
async def update_city(new_city: City, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_city, session)
    return result


# Метод для удаления города из базы данных по id
@router.delete("/")
async def delete_city(city_id: int, entity: CRUDableEntity = Depends(lambda: city), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(city_id, session)
    return result

