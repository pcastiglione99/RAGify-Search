import os
import re
import base64
from langchain_core.callbacks import file
import requests
from bs4 import BeautifulSoup
from langchain_core.vectorstores import InMemoryVectorStore
from googlesearch import search
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama

def fetch_web_pages(query: str, download_dir: str = "./downloaded"):
    os.makedirs(download_dir, exist_ok=True)
    for result in search(query, lang="en", region="us"):
        try:
            response = requests.get(result, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.find("body").get_text(strip=True)
            text = re.sub(r'\s{2,}', '\n', text)

            local_filename = base64.b64encode(result.encode("utf-8")).decode()
            with open(os.path.join(download_dir, local_filename), "w", encoding="utf-8") as f:
                f.write(text)
        except (requests.RequestException, AttributeError):
            continue

def load_documents(download_dir: str = "./downloaded") -> list[Document]:
    loader = DirectoryLoader(download_dir)
    return loader.load()

def split_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    return text_splitter.split_documents(documents)

def get_embedding_function(model_name: str = "nomic-embed-text"):
    return OllamaEmbeddings(model=model_name)

def add_to_db(chunks: list[Document], embedding_function) -> InMemoryVectorStore:
    db = InMemoryVectorStore(embedding=embedding_function)
    db.add_documents(chunks)
    return db

def query_RAG(query: str, model_name: str = "llama3.2", download_dir: str = "./downloaded") -> str:
    fetch_web_pages(query, download_dir)
    documents = load_documents(download_dir)
    chunks = split_documents(documents)

    embedding_function = get_embedding_function()
    db = add_to_db(chunks, embedding_function)
    results = db.similarity_search_with_score(query, k=3)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt_template = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the following context:

        {context}

        ---

        Answer the question based on the above context. Write at least 5 lines. Do
        not write "according to the context", just write the answer: {question}
        """
    )

    prompt = prompt_template.format(context=context_text, question=query)
    model = ChatOllama(model=model_name)
    response_text = model.invoke(prompt)

    sources = [base64.b64decode(doc.metadata.get("source", "Unknown")[11:]).decode() for doc, _score in results]

    formatted_response = f"{response_text.content}\nSources: {sources}"
    return formatted_response

def remove_temp_files(download_dir: str = "./downloaded"):
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        os.remove(file_path)

def main(query_text: str) -> str:
    try:
        response = query_RAG(query_text)
    finally:
        remove_temp_files()
    return response
