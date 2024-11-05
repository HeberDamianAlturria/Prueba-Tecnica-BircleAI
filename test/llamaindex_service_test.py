import os
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


# Mocked VectorStoreIndex class. This is used to mock the VectorStoreIndex.from_documents method.
class MockedVectorStoreIndex:
    def as_query_engine(self):
        return "Mocked query engine."


@pytest.fixture
def llama_index_instance():
    """Fixture to return the LlamaIndexSingleton instance."""
    instance = _LlamaIndexSingleton()
    instance._index = None
    yield instance


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


def assert_llm_configured(mock_settings):
    """Helper function to assert LLM configuration."""
    assert mock_settings.llm is not None, "LLM should be configured."
    assert isinstance(mock_settings.llm, Groq), "LLM should be an instance of Groq."


def assert_embedding_configured(mock_settings):
    """Helper function to assert embedding model configuration."""
    assert (
        mock_settings.embed_model is not None
    ), "Embedding model should be configured."
    assert isinstance(
        mock_settings.embed_model, HuggingFaceEmbedding
    ), "Embedding model should be an instance of HuggingFaceEmbedding."


def assert_index_initialized():
    """Helper function to assert index is initialized."""
    instance = _LlamaIndexSingleton()
    assert instance._index is not None, "Index should be initialized."
    assert isinstance(
        instance._index, MockedVectorStoreIndex
    ), "Index should be an instance of VectorStoreIndex."


def assert_query_engine(query_engine):
    """Helper function to assert query engine."""
    assert (
        query_engine == "Mocked query engine."
    ), "Query engine should be the mocked value."


def test_llama_index_singleton_instance():
    """Test that the singleton instance is the same."""
    instance1 = _LlamaIndexSingleton()
    instance2 = _LlamaIndexSingleton()
    assert instance1 is instance2, "Singleton instances should be identical."


def test_configure_llm_no_api_key(llama_index_instance):
    """Test configure LLM without API key."""
    with patch.dict(os.environ, {GROQ_API_KEY_ENV_VAR: ""}):
        with pytest.raises(RuntimeError, match=GROQ_API_KEY_ERROR):
            llama_index_instance._configure_llm()


def test_configure_llm_with_api_key(llama_index_instance, mock_settings):
    """Test configure LLM with API key."""
    with patch.dict(os.environ, {GROQ_API_KEY_ENV_VAR: "test_key"}):
        llama_index_instance._configure_llm()
        assert_llm_configured(mock_settings)


def test_configure_embedding(llama_index_instance, mock_settings):
    """Test configure embedding."""
    llama_index_instance._configure_embedding()
    assert_embedding_configured(mock_settings)


def test_initialize_llama_index(
    llama_index_instance, mock_settings, mock_from_documents
):
    """Test initialize llama index."""
    with patch.dict(os.environ, {GROQ_API_KEY_ENV_VAR: "test_key"}):
        llama_index_instance.initialize()

        assert_llm_configured(mock_settings)
        assert_embedding_configured(mock_settings)
        assert_index_initialized()


def test_get_query_engine_index_not_initialized(llama_index_instance):
    """Test get query engine if index is not initialized."""
    with pytest.raises(RuntimeError, match="Index is not initialized."):
        llama_index_instance.get_query_engine()


def test_get_query_engine_index_initialized(
    llama_index_instance, mock_settings, mock_from_documents
):
    """Test get query engine if index is initialized."""
    llama_index_instance.initialize()

    query_engine = llama_index_instance.get_query_engine()
    assert_query_engine(query_engine)


def test_initialize_llamaindex(mock_settings, mock_from_documents):
    """Test initialize llama index function."""
    initilize_llamaindex()

    assert_llm_configured(mock_settings)
    assert_embedding_configured(mock_settings)
    assert_index_initialized()


def test_provide_query_engine_index_not_initialized(llama_index_instance):
    """Test provide query engine if index is not initialized."""
    with pytest.raises(RuntimeError, match="Index is not initialized."):
        provide_query_engine()


def test_provide_query_engine(mock_settings, mock_from_documents):
    """Test provide query engine."""
    initilize_llamaindex()

    query_engine = provide_query_engine()
    assert_query_engine(query_engine)
