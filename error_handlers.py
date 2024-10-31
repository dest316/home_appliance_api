from fastapi import Request, HTTPException
from sqlalchemy.exc import IntegrityError, DBAPIError


async def FKVError_handler(request: Request, exc: IntegrityError):
    """
    Асинхронный обработчик ошибок IntegrityError для FastAPI.

    Функция отлавливает любые ошибки IntegrityError во всем API, отдельно выделяя ошибку при удалении записи, с которой связаны данные
    в других таблицах и ошибку указания в качестве внешнего ключа id несуществующего объекта. В этих случаях будет выброшено исключение
    HTTPException с кодом 404 для предоставления пользователю информации об ошибке. В случае, если IntegrityError возникнет по другой причине,
    пользователь получит ошибку 500.

    Параметры:
    ----------
    request : Request
        HTTP-запрос, в результате которого возникло исключение IntegrityError.
    exc : IntegrityError
        Выброшенное исключение IntegrityError

    Возвращает:
    -----------
    None

    Исключения:
    -----------
    HTTPException
    """
    error_message = str(exc.orig).lower()
    if 'update or delete' in error_message or "update или delete" in error_message:
        raise HTTPException(status_code=400, detail="Попытка удаления объекта, на который есть ссылки в базе данных")
    elif 'foreign key constraint' in error_message or "ограничение внешнего ключа" in error_message:
        raise HTTPException(status_code=400, detail="Внешний ключ ссылается на несуществующий объект.")
    else:
        raise HTTPException(status_code=500, detail=f"Что-то пошло не так, текст ошибки: {error_message}")
    

async def DBApiError_handler(request: Request, exc: DBAPIError):
    error_message = str(exc.orig).lower()
    if "can't subtract offset-naive and offset-aware datetimes" in error_message:
        raise HTTPException(400, detail={"message": "Дата отправлена в неправильном формате. Рекомендуется использовать дату следующего\
 формата: YYYY-MM-ddТhh:mm:ss.f"})
    else:
        raise HTTPException(status_code=500, detail=f"Что-то пошло не так, текст ошибки: {error_message}")