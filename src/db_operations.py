from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from config import EMBEDDING_MODEL_NAME

def get_embedding_function(model_name: str = EMBEDDING_MODEL_NAME):
    return OllamaEmbeddings(model=model_name)

def add_to_db(chunks, embedding_function) -> InMemoryVectorStore:
    db = InMemoryVectorStore(embedding=embedding_function)
    db.add_documents(chunks)
    return db
