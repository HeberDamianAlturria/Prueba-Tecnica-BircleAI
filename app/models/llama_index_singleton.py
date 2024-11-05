from app.constants.llama_index_constants import GROQ_MODEL, EMBEDDING_MODEL, DATA_PATH
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
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

    def _get_documents(self):
        parser = FlatReader()

        file_extractor = {".txt": parser}

        documents = SimpleDirectoryReader(
            input_dir=DATA_PATH, file_extractor=file_extractor
        ).load_data()

        return documents

    def _configure_llm(self):
        api_key = os.getenv("GROQ_API_KEY")

        if api_key is None:
            raise RuntimeError("GROQ_API_KEY is not set in the environment variables.")

        groq_llm = Groq(model=GROQ_MODEL, api_key=api_key)
        Settings.llm = groq_llm

    def _configure_embedding(self):
        hugginface_embedding = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
        Settings.embed_model = hugginface_embedding

    def initialize(self):
        self._configure_llm()
        self._configure_embedding()
        documents = self._get_documents()
        self._index = VectorStoreIndex.from_documents(documents, show_progress=True)

    def get_query_engine(self) -> BaseQueryEngine:
        if self._index is None:
            raise RuntimeError("Index is not initialized.")
        return self._index.as_query_engine()


def provide_query_engine() -> BaseQueryEngine:
    return _LlamaIndexSingleton().get_query_engine()

def initilize_llama_index():
    _LlamaIndexSingleton().initialize()
