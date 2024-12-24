from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from config import MODEL_NAME

def extract_keywords(query: str) -> list[str]:
    system_prompt = ChatPromptTemplate.from_template('''
You are a query generator designed to assist with web searches. Your task is to take a user query and generate one or more precise, relevant queries to be input into a web search engine. These queries should aim to retrieve the most authoritative, comprehensive, and contextually relevant web pages to answer the user's original question effectively.
---
Requirements:

    Understand the Query: Analyze the user query to understand its intent, context, and key terms.
    Generate Specific Queries: Transform the user's query into one or more specific and optimized search engine queries. Include synonyms, related terms, and clarifying phrases where necessary to maximize relevance.
    Maintain Precision: Avoid overly broad or ambiguous terms. Focus on generating queries that are likely to return high-quality, targeted results.
    Prioritize Relevance: Tailor the queries to address the primary information need of the user, ensuring that the resulting webpages are likely to contain accurate and useful information.
    Output Structure: Provide each query on a new line. Generate ONLY the list of queries for each input.
---
Example:

    Input Query: "What are the benefits of interval training for runners?"
    Output:
        Benefits of interval training for runners
        Interval training advantages for long-distance runners
        Scientific studies on interval training for running performance
        How interval workouts improve endurance and speed for runners
---
Make sure the queries are diverse enough to cover different aspects of the topic while remaining relevant to the original query.
---
**Input Query:** {input_query}

**Output:**
    ''')

    llm = ChatOllama(model=MODEL_NAME)
    prompt = system_prompt.format(input_query=query)

    llm_output = llm.invoke(prompt)

    keywords = llm_output.content.splitlines()


    return keywords