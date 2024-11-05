from fastapi import FastAPI
from app.routers.query_routes import query_router

app = FastAPI()

app.include_router(query_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
