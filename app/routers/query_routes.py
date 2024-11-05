from fastapi import APIRouter

query_router = APIRouter()


@query_router.get("/query")
def handle_query(q: str):
    return {"query": q}
