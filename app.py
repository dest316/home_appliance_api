from fastapi import FastAPI
from fastapi import Response
from api.controllers.crud_city import router as crud_city_router
from api.controllers.crud_product import router as crud_product_router
from api.controllers.crud_store import router as crud_store_router
from api.controllers.crud_trade import router as crud_trade_router
from api.controllers.specific_trade import router as spec_trade_router
from error_handlers import FKVError_handler, DBApiError_handler
from sqlalchemy.exc import IntegrityError, DBAPIError


# Точка входа в API
app = FastAPI(
    title="API"
)


# Подключение роутеров с маршрутами для API
app.include_router(crud_city_router)
app.include_router(crud_product_router)
app.include_router(crud_store_router)
app.include_router(crud_trade_router)
app.include_router(spec_trade_router)


# Подключение обработчиков ошибок
app.add_exception_handler(IntegrityError, FKVError_handler)
app.add_exception_handler(DBAPIError, DBApiError_handler)

# Главная страница приложения
@app.get('/')
def index():
    return Response("Hello world")

