from langchain_core.vectorstores import InMemoryVectorStore

from googlesearch import search

from langchain_community.document_loaders import DirectoryLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.schema.document import Document

from langchain_ollama import OllamaEmbeddings

from langchain.prompts import ChatPromptTemplate

from langchain_ollama.chat_models import ChatOllama

import argparse
import os

import requests
from bs4 import BeautifulSoup
import base64
import re

QUERY="what is retrieval augmented generation"

def fetch_web_pages(QUERY: str):
    results = search(QUERY, 
                    lang="en", 
                    region="us")


    for result in list(results):
        with requests.get(result) as r:
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.find("body").get_text()
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r'\t\s*\t', '\t\t', text)
            #text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
            local_filename = base64.b64encode(result.encode("utf-8")).decode()
            with open(f"./downloaded/{local_filename}", "w") as f:
                f.write(text)

def load_documents():
    loader = DirectoryLoader("./downloaded")
    documents = loader.load()
    return documents

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

def get_embedding_function(model_name: str =  "nomic-embed-text"):
    embeddings = OllamaEmbeddings(
    model = model_name
    )
    return embeddings


def add_to_db(chunks: list[Document], embedding_function):
    db = InMemoryVectorStore(
        embedding = embedding_function
    )
    db.add_documents(chunks)
    return db



def query_RAG(QUERY: str):

    fetch_web_pages(QUERY)
    web_pages = load_documents()
    chunks = split_documents(documents = web_pages)
    db = add_to_db(chunks = chunks, embedding_function=get_embedding_function())
    results= db.similarity_search_with_score(QUERY, k=5)

    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    prompt = prompt_template.format(context=context_text, question=QUERY)

    model = ChatOllama(model="llama3.2")
    response_text = model.invoke(prompt)

    sources = [base64.b64decode(doc.metadata.get("source", "Unknown")[11:]).decode() for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"

    print(formatted_response)


def remove_temp_files():
    for filename in os.listdir("./downloaded"):
        file_path = os.path.join("./downloaded", filename)
        os.remove(file_path) 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_RAG(query_text)
    remove_temp_files()


if __name__ == "__main__":
    main()
    remove_temp_files()
