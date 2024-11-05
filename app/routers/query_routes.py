from app.models.llama_index_singleton import provide_query_engine
from app.DTOs.query_response_dto import QueryResponseDTO
from llama_index.core.query_engine import BaseQueryEngine
from fastapi import APIRouter, Depends, HTTPException

query_router = APIRouter()


@query_router.get(
    "/query",
    summary="Execute a query against the Llama Index",
    description=(
        "This endpoint allows users to submit a query string to the Llama Index. "
        "The query is processed using the underlying vector store index, and the results "
        "are returned as a response."
    ),
    response_description="The response contains the results of the query.",
    response_model=QueryResponseDTO,
    responses={
        400: {"description": "Query is required and cannot be empty."},
        500: {"description": "An error occurred while processing the query."},
    },
)
def handle_query(
    q: str, query_engine: BaseQueryEngine = Depends(provide_query_engine)
) -> QueryResponseDTO:
    """
    Execute a user query against the Llama Index.

    Args:
        q (str): Non-empty query string.
        query_engine (BaseQueryEngine): Dependency-injected query engine.

    Returns:
        dict: Results of the query.

    Raises:
        HTTPException:
            - 400 if the query string is empty.
            - 500 if there is an error processing the query.
    """
    if not q.strip():
        raise HTTPException(
            status_code=400, detail="Query is required and cannot be empty."
        )

    try:
        result = query_engine.query(q)
        return QueryResponseDTO(response=result.response)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your query."
        )
