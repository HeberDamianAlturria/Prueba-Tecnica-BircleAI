from app.routers.query_routes import query_router
from app.lifespan import app_lifespan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BircleAI Technical Test",
    description="This is the API documentation for the BircleAI Technical Test.",
    version="0.1",
    lifespan=app_lifespan,
)

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
