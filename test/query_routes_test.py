import pytest
from fastapi.testclient import TestClient
from app.routers.query_routes import query_router
from app.services.llamaindex_service import provide_query_engine
from app.DTOs.query_response_dto import QueryResponseDTO
from app.constants.query_error_messages import (
    EMPTY_QUERY_ERROR_MESSAGE,
    QUERY_PROCESSING_FAILURE_MESSAGE,
)
from fastapi import FastAPI, status

# Configure FastAPI application and include the query router.
app = FastAPI()
app.include_router(query_router)
client = TestClient(app)

# Constants for mocks.
ERROR_SIMULATION_QUERY = "error"  # Query string that simulates an error condition.


def get_mock_message(q: str) -> str:
    """Generate a mock response message for a given query."""
    return f"Mock response for query: {q}"


# Mock class to simulate the behavior of the query response.
class MockQueryResponse:
    def __init__(self, response: str):
        self.response = response


# Mock class to simulate the behavior of the query engine.
class MockQueryEngine:
    def query(self, q: str):
        if q == ERROR_SIMULATION_QUERY:  # Simulate an error condition.
            raise Exception("Mock error")
        return MockQueryResponse(response=get_mock_message(q))


@pytest.fixture
def override_provide_query_engine():
    """Fixture to override the provide_query_engine dependency with a mock."""
    app.dependency_overrides[provide_query_engine] = lambda: MockQueryEngine()
    yield
    app.dependency_overrides.clear()


def test_handle_query_success(override_provide_query_engine):
    """Test handling of a successful query."""
    q = "test"
    response = client.get(f"/query?q={q}")
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json() == QueryResponseDTO(response=get_mock_message(q)).model_dump()
    )


def test_handle_query_empty_query(override_provide_query_engine):
    """Test handling of an empty query."""
    response = client.get("/query?q=")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": EMPTY_QUERY_ERROR_MESSAGE}


def test_handle_query_error(override_provide_query_engine):
    """Test handling of a query processing error."""
    response = client.get(f"/query?q={ERROR_SIMULATION_QUERY}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": QUERY_PROCESSING_FAILURE_MESSAGE}
