from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from googlesearch import search
from config import REQUESTS_HEADER

def web_search(queries: list[str], num_results: int) -> list[Document]:
    for query in queries:
        urls = list(search(query, num_results=num_results, lang="en", region="us"))
        print(urls)
    loader = WebBaseLoader(urls,header_template=REQUESTS_HEADER)
    docs = loader.aload()
    return docs