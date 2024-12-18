import streamlit as st
import main


st.title("RAGify")



if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    response = main.main(prompt)
    st.chat_message("assistant").write(response)
