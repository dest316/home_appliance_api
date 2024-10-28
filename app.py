from fastapi import FastAPI
from fastapi import Response
from api.controllers.crud_city import router as crud_city_router
from api.controllers.crud_product import router as crud_product_router
from api.controllers.crud_store import router as crud_store_router
from api.controllers.crud_trade import router as crud_trade_router
from api.controllers.specific_trade import router as spec_trade_router


app = FastAPI(
    title="API"
)

app.include_router(crud_city_router)
app.include_router(crud_product_router)
app.include_router(crud_store_router)
app.include_router(crud_trade_router)
app.include_router(spec_trade_router)


@app.get('/')
def index():
    return Response("Hello world")

