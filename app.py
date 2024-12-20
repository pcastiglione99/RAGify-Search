import streamlit as st
from langchain_ollama.chat_models import ChatOllama
from nlp_utils import extract_keywords
from web_scraper import fetch_web_pages, remove_temp_files
from db_operations import get_embedding_function
from prompt_generator import generate_prompt


def chunk_generator(llm, query):
    for chunk in llm.stream(query):
        yield chunk

st.title("RAGify")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if usr_msg := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": usr_msg})
    st.chat_message("user").write(usr_msg)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("model working..."):
            keywords = extract_keywords(usr_msg)
            fetch_web_pages(keywords)

            embedding_function = get_embedding_function()
            
            prompt, sources = generate_prompt(usr_msg, embedding_function)

            llm = ChatOllama(model="llama3.2", stream=True)

            stream_data = chunk_generator(llm, prompt)
            st.write_stream(stream_data)
            st.write(sources)
