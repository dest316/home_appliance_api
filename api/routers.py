from fastapi import APIRouter, Depends
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from models.models import cities
from typing import List
from schemas.schemas import City


router = APIRouter(
    prefix='/api',
    tags=["CRUD_operations"]
)

@router.get("/")
async def get_city(session: AsyncSession = Depends(get_async_session)):
    query = select(cities)
    result = await session.execute(query)
    return list(result.mappings())


# To-do: Добавить проверку на уникальность id, по-хорошему сделать уникальным так же и название города, и не добавлять id в запросе
# т.к. он автоматически генерируется в бд
@router.post("/")
async def add_city(new_city: City, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(cities).values(**new_city.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
    

