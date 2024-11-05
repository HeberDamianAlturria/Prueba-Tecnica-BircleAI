from app.routers.query_routes import query_router
from app.models.llama_index_singleton import initilize_llama_index
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    initilize_llama_index()
    yield


app = FastAPI(title="BircleAI Technical Test", lifespan=app_lifespan)

# Add CORS middleware to allow requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
