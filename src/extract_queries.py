from pydantic import BaseModel 
from config import MODEL_NAME, PROMPT
from ollama import chat
from datetime import datetime
import json

class Queries(BaseModel):
    queries: list[str]

def extract_queries(query: str, model: str = MODEL_NAME) -> list[str]:
    """
    Extracts a list of queries from the given user query.

    Args:
        query (str): The user's input query.
        model (str, optional): The language model to use. Defaults to the value in config.MODEL_NAME.
        
    Returns:
        List[str]: A list of extracted queries.
    """
    response = chat(
        model=model,
        messages=[{"role": "user", "content": PROMPT.format(date=datetime.today().strftime('%Y-%m-%d'), input_query=query)}],
        options={"temperature":0.2},
        format=Queries.model_json_schema()
    )

    queries = response['message']['content']

    queries = json.loads(queries)
    return queries["queries"]