from googlesearch import search
from langchain_community.document_loaders import WebBaseLoader

QUERY="what is retrieval augmented generation"

results = list(search(QUERY))

loader = WebBaseLoader(results)

docs = loader.load()

