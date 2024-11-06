# API Key environment variable name.
GROQ_API_KEY_ENV_VAR = "GROQ_API_KEY"

# Error message for missing API key environment variable.
GROQ_API_KEY_ERROR = f"{GROQ_API_KEY_ENV_VAR} is not set in the environment variables."

# Model and data paths for the LlamaIndex.
GROQ_MODEL = "llama3-70b-8192"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
DATA_PATH = "./app/data"
EXTENSION_FILES_ALLOWED = [".txt"]
