from fastapi import Request, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse


def FKVError_handler(request: Request, exc: IntegrityError):
    error_message = str(exc.orig).lower()
    if 'foreign key constraint' in error_message or "ограничение внешнего ключа" in error_message:
        raise HTTPException(status_code=400, detail="Ссылка на несуществующий объект.")
    elif 'referential integrity violation' in error_message or 'нарушение ссылочной целостности' in error_message:
        raise HTTPException(status_code=400, detail="Попытка удаления объекта, на который есть ссылки в базе данных")
    else:
        raise HTTPException(status_code=500, detail=f"Что-то пошло не так, текст ошибки: {error_message}")