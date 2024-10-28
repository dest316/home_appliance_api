from api.controllers.utils import CRUDableEntity
from schemas.product import Product, WriteProduct
from models.models import products
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import List


router = APIRouter(
    prefix='/api/product',
    tags=["CRUD_product"]
)

product = CRUDableEntity(Product, WriteProduct, products)

@router.get("/", response_model=Product)
async def get_specific_product(product_id: int, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get(product_id, session)
    return result


@router.get("/all", response_model=List[Product])
async def get_products(entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.get_all(session)
    return result


@router.post("/")
async def add_product(new_product: Product, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.post(new_product, session)
    return result

@router.put("/")
async def update_product(new_product: Product, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.put(new_product, session)
    return result

@router.delete("/")
async def delete_product(product_id: int, entity: CRUDableEntity = Depends(lambda: product), session: AsyncSession = Depends(get_async_session)):
    result = await entity.delete(product_id, session)
    return result