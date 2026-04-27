# Local LLM CS Tutor with Hybrid RAG (Ollama, FastAPI, React)

## Overview

This project is an end-to-end AI Knowledge Assistant built using a local large language model with Ollama (Llama 3.2). It acts as a Computer Science tutor that provides structured academic answers and supports document-based question answering using a complete Retrieval-Augmented Generation pipeline. The system includes hybrid retrieval, conversation memory, query rewriting, and a developer mode for debugging internal operations. It consists of a Python backend and a React frontend interface.

## Features

The assistant generates answers in a structured format including Definition, Explanation, Example, Advantages, and Disadvantages. It uses a local LLM via Ollama, eliminating dependency on external APIs. The system supports PDF ingestion and extracts text from documents for further processing. It implements document chunking and hybrid retrieval combining semantic search using vector databases and keyword-based retrieval. Retrieved context is injected into prompts to generate accurate answers. The system includes query rewriting to improve retrieval quality. Conversation memory enables multi-turn context-aware interactions. A developer mode is available to inspect retrieved chunks, similarity scores, rewritten queries, and internal logs. The frontend provides a responsive chat interface with chat history and debugging panel.

## Project Structure

The project is organized into backend modules, RAG pipeline components, memory handling, and a React frontend.

project/
app/
memory/
chat_memory.py
db.py
data/
os_notes.pdf
rag/
ingest.py
retrieve.py
query_rewrite.py
rag-frontend/
src/
components/
ChatWindow.js
DevPanel.js
MessageBubble.js
Sidebar.js
ToggleSwitch.js
services/
public/
requirements.txt

## Installation

Install Ollama and ensure it is available on your system. Pull the model using the command `ollama pull llama3.2`. Install Python dependencies using `pip install -r requirements.txt`. The requirements include flask-cors, numpy, scikit-learn, faiss-cpu, requests, gunicorn, sentence-transformers, and openai. Navigate to the rag-frontend folder and install frontend dependencies using `npm install`.

## Running the Application

Start the Ollama server using `ollama serve`. Run the backend server using your Python entry point or API server configuration. Navigate to the rag-frontend directory and start the frontend using `npm start`. Open the browser to access the chat interface.

## Usage

Users can ask Computer Science questions and receive structured academic answers. The assistant can read PDF documents and answer questions based on their content using the RAG pipeline. Follow-up questions are handled using conversation memory. Developer mode can be enabled to view internal retrieval and reasoning steps.

## Architecture

The system processes a user query through query rewriting, followed by hybrid retrieval combining vector similarity search and keyword-based search. The top relevant document chunks are selected and passed into a structured prompt. This prompt is sent to the local LLM through Ollama, which generates the final response. The backend returns the answer along with optional debug data to the frontend.

Flow:
User Query → Query Rewrite → Hybrid Retrieval → Top-K Chunks → Prompt Construction → LLM → Response

## Tech Stack

Python is used for backend development. Ollama is used to run the Llama 3.2 model locally. LangChain and sentence-transformers are used for RAG and embeddings. FAISS is used for vector search. BM25 or keyword search is used for lexical retrieval. React is used for the frontend interface.

## Key Highlights

The project demonstrates prompt engineering for controlling LLM output, local deployment of language models, implementation of a hybrid RAG pipeline, query rewriting for improved retrieval, conversation memory for contextual understanding, and a developer mode for debugging. It is a complete full-stack AI system.

## Project Status

All core components including local LLM integration, PDF ingestion, hybrid retrieval, query rewriting, conversation memory, frontend UI, and developer mode are implemented. The system is fully functional.

## Author

Praharshitha

## License

This project is intended for educational and demonstration purposes.
