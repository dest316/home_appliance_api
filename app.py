from fastapi import FastAPI
from fastapi import Response
from api.routers import router as api_router


app = FastAPI(
    title="API"
)

app.include_router(api_router)

@app.get('/')
def index():
    return Response("Hello world")

