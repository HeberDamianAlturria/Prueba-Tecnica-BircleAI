import pytest
from unittest.mock import patch
from app.services.llamaindex_service import (
    _LlamaIndexSingleton,
    provide_query_engine,
    initilize_llamaindex,
)
from app.constants.llamaindex_constants import GROQ_API_KEY_ENV_VAR, GROQ_API_KEY_ERROR
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os


class MockedVectorStoreIndex:
    def as_query_engine(self):
        return "Mocked query engine."


@pytest.fixture
def mock_settings():
    """Fixture to mock the Settings object."""
    with patch("app.services.llamaindex_service.Settings") as mock:
        mock.llm = None
        mock.embed_model = None
        yield mock


@pytest.fixture
def mock_from_documents():
    """Fixture to mock the VectorStoreIndex.from_documents method."""
    with patch(
        "app.services.llamaindex_service.VectorStoreIndex.from_documents"
    ) as mock:

        mock.return_value = MockedVectorStoreIndex()
        yield mock


# Test the singleton instance of the Llama Index.
def test_llama_index_singleton_instance():
    instance1 = _LlamaIndexSingleton()
    instance2 = _LlamaIndexSingleton()
    assert instance1 is instance2, "Singleton instances should be identical."


# Test raise error if not api key.
def test_configure_llm_no_api_key():
    # Set the environment variable to an empty string.
    with patch.dict(os.environ, {GROQ_API_KEY_ENV_VAR: ""}):
        instance = _LlamaIndexSingleton()
        with pytest.raises(RuntimeError, match=GROQ_API_KEY_ERROR):
            instance._configure_llm()


# Test if API key is set.
def test_configure_llm_with_api_key(mock_settings):
    # Set the environment variable to a test value.
    with patch.dict(os.environ, {GROQ_API_KEY_ENV_VAR: "test_key"}):
        instance = _LlamaIndexSingleton()
        instance._configure_llm()

        # After configuration, llm should no longer be None and should be an instance of Groq.
        assert mock_settings.llm is not None, "LLM should be configured."

        assert isinstance(mock_settings.llm, Groq), "LLM should be an instance of Groq."


# Test configure embedding.
def test_configure_embedding(mock_settings):
    instance = _LlamaIndexSingleton()
    instance._configure_embedding()

    # After configuration, embed_model should no longer be None.
    assert (
        mock_settings.embed_model is not None
    ), "Embedding model should be configured."

    assert isinstance(
        mock_settings.embed_model, HuggingFaceEmbedding
    ), "Embedding model should be an instance of HuggingFaceEmbedding."


# Test initialize llama index.
def test_initialize_llama_index(mock_settings, mock_from_documents):
    # Set up the environment variable with a test API key.
    with patch.dict(os.environ, {GROQ_API_KEY_ENV_VAR: "test_key"}):
        instance = _LlamaIndexSingleton()
        instance.initialize()  # Initialize the instance, which will configure LLM and embedding.

        # Check that the LLM has been configured correctly.
        assert (
            mock_settings.llm is not None
        ), "LLM should be configured after initialization."
        assert isinstance(mock_settings.llm, Groq), "LLM should be an instance of Groq."

        # Check that the embedding model has been configured correctly.
        assert (
            mock_settings.embed_model is not None
        ), "Embedding model should be configured after initialization."
        assert isinstance(
            mock_settings.embed_model, HuggingFaceEmbedding
        ), "Embedding model should be an instance of HuggingFaceEmbedding."

        # Check that the index has been initialized with the mocked return value.
        assert (
            instance._index is not None
        ), "Index should be initialized with the mocked return value."

        assert isinstance(
            instance._index, MockedVectorStoreIndex
        ), "Index should be an instance of VectorStoreIndex."


# Test get query engine if index is not initialized.
def test_get_query_engine_index_not_initialized():
    # Initialize index as None to simulate unconfigured state.
    instance = _LlamaIndexSingleton()
    instance._index = None

    with pytest.raises(RuntimeError, match="Index is not initialized."):
        instance.get_query_engine()


# Test get query engine if index is initialized.
def test_get_query_engine_index_initialized(mock_settings, mock_from_documents):
    instance = _LlamaIndexSingleton()
    instance.initialize()  # Initialize the index to simulate a configured state.

    query_engine = instance.get_query_engine()
    assert query_engine is not None, "Query engine should be returned."
    assert (
        query_engine == "Mocked query engine."
    ), "Query engine should be the mocked value."


# Test initialize llama index function.
def test_initialize_llamaindex(mock_settings, mock_from_documents):
    initilize_llamaindex()

    # Check that the LLM has been configured correctly.
    assert (
        mock_settings.llm is not None
    ), "LLM should be configured after initialization."
    assert isinstance(mock_settings.llm, Groq), "LLM should be an instance of Groq."

    # Check that the embedding model has been configured correctly.
    assert (
        mock_settings.embed_model is not None
    ), "Embedding model should be configured after initialization."
    assert isinstance(
        mock_settings.embed_model, HuggingFaceEmbedding
    ), "Embedding model should be an instance of HuggingFaceEmbedding."

    # Check that the index has been initialized with the mocked return value.
    assert (
        _LlamaIndexSingleton()._index is not None
    ), "Index should be initialized with the mocked return value."

    assert isinstance(
        _LlamaIndexSingleton()._index, MockedVectorStoreIndex
    ), "Index should be an instance of VectorStoreIndex."


# Test provide query engine if index is not initialized.
def test_provide_query_engine_index_not_initialized():
    # Initialize index as None to simulate unconfigured state.
    instance = _LlamaIndexSingleton()
    instance._index = None

    with pytest.raises(RuntimeError, match="Index is not initialized."):
        provide_query_engine()


# Test provide query engine.
def test_provide_query_engine(mock_settings, mock_from_documents):
    initilize_llamaindex()

    query_engine = provide_query_engine()
    assert query_engine is not None, "Query engine should be returned."
    assert (
        query_engine == "Mocked query engine."
    ), "Query engine should be the mocked value."
