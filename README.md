# RAGify Search - Intelligent Assistant with Web Search RAG

## Description
RAGify Search is an AI-powered intelligent assistant built with Streamlit, designed to answer user queries by integrating real-time web search, natural language processing (NLP), and advanced embedding techniques. It uses a Retrieval-Augmented Generation (RAG) approach to provide accurate, concise, and context-aware responses

---

## Key Features
- **Real-Time Web Search**: Fetch relevant web pages for user queries.
- **NLP-Based Keyword Extraction**: Leverage NLTK to identify key terms for targeted searches.
- **Document Processing**: Split, embed, and index documents for similarity-based searches.
- **Prompt Engineering**: Generate optimized prompts for the LLM model.
- **Streamlit Interface**: Simple and intuitive chatbot-like user experience.
- **Temporary File Management**: Automatic cleanup of downloaded content to save space.
- **Local LLM Support**: Utilizes Ollama to run a local LLM, ensuring data privacy and high performance.

---

## Directory Structure

- **`web_scraper.py`**: Manages web scraping and temporary file handling.
- **`nlp_utils.py`**: Extracts keywords using advanced NLP techniques.
- **`db_operations.py`**: Embeds and indexes document chunks for search.
- **`prompt_generator.py`**: Prepares structured prompts for context-aware answers.
- **`app.py`**: Front-end application powered by Streamlit.
- **`config.py`**: Centralized configuration for chunk sizes, model names, and directories.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pcastiglione99/RAGify-Search.git
   cd RAGify-Search
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run ./src/app.py
   ```

---

## Usage

1. Start the Streamlit app and interact with the chatbot.
2. Enter your query in the chat interface.
3. The assistant fetches web pages, processes content, and generates a response.

