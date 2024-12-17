from langchain_core.vectorstores import InMemoryVectorStore
import nest_asyncio
nest_asyncio.apply()
from googlesearch import search
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings

from langchain.prompts import ChatPromptTemplate

from langchain_ollama.chat_models import ChatOllama

QUERY="what is retrieval augmented generation"

def load_web_pages(QUERY: str):
    results = [ str(res) for res in search(QUERY) ]
    loader = WebBaseLoader(results)
    return loader.aload()

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

    web_pages = load_web_pages(QUERY)
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

    sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"

    print(formatted_response)


if __name__ == "__main__":
    query_RAG(QUERY)
