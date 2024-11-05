from app.routers.query_routes import query_router
from app.models.llama_index_singleton import LlamaIndexSingleton
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    LlamaIndexSingleton().initialize()
    yield
    LlamaIndexSingleton().close()


app = FastAPI(lifespan=app_lifespan)

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
