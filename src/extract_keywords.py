from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from config import MODEL_NAME, PROMPT

def extract_keywords(query: str, model: str = MODEL_NAME) -> list[str]:
    system_prompt = ChatPromptTemplate.from_template(PROMPT)

    llm = ChatOllama(model=model)
    prompt = system_prompt.format(input_query=query)

    llm_output = llm.invoke(prompt)

    keywords = llm_output.content.splitlines()


    return keywords
