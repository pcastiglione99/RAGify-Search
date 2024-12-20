import base64
from langchain_community.document_loaders import DirectoryLoader
from langchain.schema.document import Document
from langchain.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db_operations import add_to_db
from web_scraper import remove_temp_files

def load_documents(download_dir: str = "./downloaded") -> list[Document]:
    loader = DirectoryLoader(download_dir)
    return loader.load()

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    return text_splitter.split_documents(documents)

def generate_prompt(query: str, embedding_function):
    documents = load_documents()
    chunks = split_documents(documents)
    db = add_to_db(chunks, embedding_function)
    results = db.similarity_search_with_score(query, k=3)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt_template = ChatPromptTemplate.from_template(
        """
        You are an intelligent assistant designed to answer user questions accurately and concisely using the following context document.
        Context:
        {context}

        ---

        Now answer the following question: 
        {question}
        """
    )

    sources = [base64.b64decode(doc.metadata.get("source", "Unknown")[11:]).decode() for doc, _score in results]
    prompt = prompt_template.format(context=context_text, question=query)

    remove_temp_files()
    return prompt, str(sources)
