from app.models.llama_index_singleton import provide_query_engine
from fastapi import APIRouter, Depends

query_router = APIRouter()


@query_router.get("/query")
def handle_query(q: str, query_engine=Depends(provide_query_engine)):
    return query_engine.query(q)
