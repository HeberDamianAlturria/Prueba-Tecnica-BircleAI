from fastapi import FastAPI
from app.routers.query_routes import query_router
import uvicorn

app = FastAPI()

app.include_router(query_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
