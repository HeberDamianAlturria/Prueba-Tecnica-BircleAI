from app.models.llama_index_singleton import initilize_llama_index
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Asynchronous context manager that initializes the Llama index at the start
    of the application lifespan and ensures proper resource management.

    This function is called when the FastAPI application starts up. It initializes
    the Llama index using the `initialize_llama_index` function. Once the setup
    is complete, control is yielded back to the application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded back to the FastAPI application until it shuts down.
    """
    initilize_llama_index()
    yield
