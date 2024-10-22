from fastapi import FastAPI
from fastapi import Response


app = FastAPI(
    title="API"
)


@app.get('/')
def index():
    return Response("Hello world")

