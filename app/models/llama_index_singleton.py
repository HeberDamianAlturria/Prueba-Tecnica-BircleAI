from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.readers.file import FlatReader
import os


class LlamaIndexSingleton:
    _instance = None
    _index = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        api_key = os.getenv("GROQ_API_KEY")

        if api_key is None:
            raise RuntimeError("GROQ_API_KEY is not set in the environment variables.")

        groq_llm = Groq(model="llama3-70b-8192", api_key=api_key)

        hugginface_embedding = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

        Settings.llm = groq_llm
        Settings.embed_model = hugginface_embedding

        parser = FlatReader()

        file_extractor = {".txt": parser}

        documents = SimpleDirectoryReader(
            "./app/data", file_extractor=file_extractor
        ).load_data()

        self._index = VectorStoreIndex.from_documents(documents, show_progress=True)

    def get_query_engine(self):
        if self._index is None:
            raise RuntimeError("Index is not initialized.")
        return self._index.as_query_engine()

    def close(self):
        if self._index is not None:
            self._index = None


def provide_query_engine():
    return LlamaIndexSingleton().get_query_engine()
