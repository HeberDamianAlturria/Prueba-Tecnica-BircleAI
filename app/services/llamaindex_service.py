from app.constants.llamaindex_constants import (
    GROQ_API_KEY_ENV_VAR,
    GROQ_API_KEY_ERROR,
    GROQ_MODEL,
    EMBEDDING_MODEL,
    DATA_PATH,
)
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader, Document
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.readers.file import FlatReader

import os


class _LlamaIndexSingleton:
    """Singleton class for managing Llama index."""

    _instance = None
    _index = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_documents(self) -> list[Document]:
        """Load documents from the specified directory using a FlatReader.

        Returns:
            list[Document]: A list of documents loaded from the directory.

        Raises:
            ValueError: If no files are found in the directory or if the directory does not exist.
        """
        parser = FlatReader()

        file_extractor = {".txt": parser}

        documents = SimpleDirectoryReader(
            input_dir=DATA_PATH, file_extractor=file_extractor
        ).load_data()

        return documents

    def _configure_llm(self):
        """Configure the language model (LLM) using the Groq API key.

        This method initializes the Groq model with the provided API key, which must be set
        in the environment variables.

        Raises:
            RuntimeError: If the API key is not set in the environment variables.
        """
        api_key = os.getenv(GROQ_API_KEY_ENV_VAR)

        if not api_key:
            raise RuntimeError(GROQ_API_KEY_ERROR)

        groq_llm = Groq(model=GROQ_MODEL, api_key=api_key)
        Settings.llm = groq_llm

    def _configure_embedding(self):
        """
        Configure the embedding model using Hugging Face's embedding model.
        """
        hugginface_embedding = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
        Settings.embed_model = hugginface_embedding

    def initialize(self):
        """Initialize the Llama index by configuring the LLM, embedding, and loading documents.

        This method performs all necessary setup steps to prepare the Llama index
        for querying, including configuring the language model, the embedding model,
        and loading documents from the specified directory.

        Raises:
            RuntimeError: If the API key is not set in the environment variables.
            ValueError: If no documents are found in the specified directory or if the directory does not exist.
        """
        self._configure_llm()
        self._configure_embedding()
        documents = self._get_documents()
        self._index = VectorStoreIndex.from_documents(documents, show_progress=True)

    def get_query_engine(self) -> BaseQueryEngine:
        """Retrieve the query engine for the Llama index.

        Returns:
            BaseQueryEngine: The query engine instance for querying the Llama index.

        Raises:
            RuntimeError: If the index has not been initialized.
        """
        if self._index is None:
            raise RuntimeError("Index is not initialized.")
        return self._index.as_query_engine()


def provide_query_engine() -> BaseQueryEngine:
    """Provide the query engine from the Llama index singleton.

    Returns:
        BaseQueryEngine: The query engine instance.
    """
    return _LlamaIndexSingleton().get_query_engine()


def initilize_llamaindex():
    """Initialize the Llama index singleton instance and index the documents.

    This function initializes the Llama index by invoking the `initialize` method of the `_LlamaIndexSingleton`
    class, which handles the setup process for the Llama index, including configuring the LLM and embedding models,
    and loading the documents.

    Raises:
        RuntimeError: If the API key is not set in the environment variables (via the `initialize` method).
        ValueError: If no documents are found in the specified directory or if the directory does not exist (via the `initialize` method).
    """
    _LlamaIndexSingleton().initialize()
