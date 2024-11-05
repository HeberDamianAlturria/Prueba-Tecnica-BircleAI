from app.models.llama_index_singleton import provide_query_engine
from fastapi import APIRouter, Depends, HTTPException

query_router = APIRouter()


@query_router.get("/query")
def handle_query(q: str, query_engine=Depends(provide_query_engine)):
    if not q:
        raise HTTPException(status_code=400, detail="Query is required.")

    return query_engine.query(q)
