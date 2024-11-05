from app.constants.llamaindex_constants import GROQ_MODEL, EMBEDDING_MODEL, DATA_PATH
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader, Document
from llama_index.core.query_engine import BaseQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.readers.file import FlatReader

import os


class _LlamaIndexSingleton:
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
            RuntimeError: If the GROQ_API_KEY is not set in the environment variables.
        """
        api_key = os.getenv("GROQ_API_KEY")

        if api_key is None:
            raise RuntimeError("GROQ_API_KEY is not set in the environment variables.")

        groq_llm = Groq(model=GROQ_MODEL, api_key=api_key)
        Settings.llm = groq_llm

    def _configure_embedding(self):
        """
        Configure the embedding model using Hugging Face's embedding model.
        """
        hugginface_embedding = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
        Settings.embed_model = hugginface_embedding

    def initialize(self):
        """
        Initialize the Llama index by configuring the LLM, embedding, and loading documents.
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
    """
    Initialize the Llama index singleton instance and index the documents.
    """
    _LlamaIndexSingleton().initialize()
