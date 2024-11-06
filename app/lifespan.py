from app.services.llamaindex_service import initilize_llamaindex
from app.config.logging_config import setup_logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Asynchronous context manager that configures logging, loads environment variables, and initializes the Llama index
    at the start of the application lifespan, and ensures proper resource management during shutdown.

    This function is called during the FastAPI application startup. It sets up logging, loads the .env file containing
    environment variables, and initializes the Llama index using the `initialize_llamaindex` function. After completing
    the setup, control is yielded back to the FastAPI application for handling requests.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded back to the FastAPI application until it shuts down.
    """
    setup_logging()
    load_dotenv()
    initilize_llamaindex()
    yield
