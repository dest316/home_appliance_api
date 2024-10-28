from pydantic import BaseModel
from sqlalchemy import Table, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from fastapi import HTTPException


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
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail={"message": "Объекта с таким id не существует"})
        await session.commit()
        return {"status": "success"}
