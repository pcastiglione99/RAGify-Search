from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

def get_embedding_function(model_name: str = "nomic-embed-text"):
    return OllamaEmbeddings(model=model_name)

def add_to_db(chunks, embedding_function) -> InMemoryVectorStore:
    db = InMemoryVectorStore(embedding=embedding_function)
    db.add_documents(chunks)
    return db
