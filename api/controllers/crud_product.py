from api.controllers.utils import CRUDableEntity
from schemas.product import Product, WriteProduct
from models.models import products
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


# Создание роутера для операций с товарами
router = APIRouter(
    prefix='/api/product',
    tags=["CRUD_product"]
)

# Создание объекта Crudable для использования стандарной реализации CRUD-операций
product = CRUDableEntity(Product, WriteProduct, products)


# Метод возвращает товар из базы данных по id
@router.get("/", response_model=Product)
async def get_specific_product(product_id: int, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(product_id, session)
    return result


# Метод возвращает список всех товаров
@router.get("/all", response_model=List[Product])
async def get_products(entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


# Метод для создания нового товара в базе данных
@router.post("/")
async def add_product(new_product: WriteProduct, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_product, session)
    return result


# Метод для обновления информации о товаре с указанным id
@router.put("/")
async def update_product(new_product: Product, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_product, session)
    return result


# Метод для удаления товара из базы данных по id
@router.delete("/")
async def delete_product(product_id: int, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(product_id, session)
    return result