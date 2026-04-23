from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time

from llm import chat_with_model
from rag.ingest import load_pdf, split_text, create_vector_store
from rag.retrieve import retrieve_chunks
from rag.query_rewrite import rewrite_query

from app.memory.chat_memory import (
    create_session,
    get_sessions,
    get_messages,
    add_message,
    get_chat_list,
    get_history,
    update_session_title,
    get_session_message_count
)

from app.memory.db import create_tables

app = Flask(__name__)
CORS(app)

# ==============================
# INIT (only DB here)
# ==============================
create_tables()

# ❗ RAG lazy loading variables
index = None
bm25_retriever = None
stored_chunks = None

# ==============================
# LOAD RAG ONLY WHEN NEEDED
# ==============================
def initialize_rag():
    global index, bm25_retriever, stored_chunks

    if index is None:
        print("⏳ Loading RAG...")

        documents = load_pdf("data/os_notes.pdf")
        chunks = split_text(documents)

        index, bm25_retriever, stored_chunks = create_vector_store(chunks)

        print("✅ RAG Ready!")


# ==============================
# SESSION APIs
# ==============================
@app.route("/session", methods=["POST"])
def new_session():
    session_id = create_session()
    return jsonify({"session_id": session_id})


@app.route("/sessions", methods=["GET"])
def sessions():
    return jsonify({"sessions": get_sessions()})


@app.route("/messages/<int:session_id>", methods=["GET"])
def messages(session_id):
    from app.memory.chat_memory import get_session_title
    msgs = get_messages(session_id)
    title = get_session_title(session_id)
    return jsonify({"messages": msgs, "title": title})


# ==============================
# CHAT API
# ==============================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)

    question = data.get("query")
    session_id = data.get("session_id")

    if not question:
        return jsonify({"answer": "❌ Empty query"})

    try:
        # 🔥 IMPORTANT: initialize RAG here
        initialize_rag()

        chat_history = get_chat_list(session_id)
        rewritten_query = rewrite_query(question, chat_history)

        relevant_chunks, scores = retrieve_chunks(
            rewritten_query, index, stored_chunks, bm25_retriever
        )

        context = "\n\n".join(relevant_chunks)
        history = get_history(session_id)

        answer = chat_with_model(context, question, history)

        add_message(session_id, question, answer)

        # auto title
        msg_count = get_session_message_count(session_id)

        if msg_count == 1:
            title = question[:40] + ("..." if len(question) > 40 else "")
            update_session_title(session_id, title)
            session_title = title
        else:
            from app.memory.chat_memory import get_session_title
            session_title = get_session_title(session_id)

        return jsonify({
            "answer": answer,
            "chunks": relevant_chunks,
            "scores": scores,
            "rewritten_query": rewritten_query,
            "session_title": session_title
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"answer": "❌ Backend error"})


# ==============================
# STREAM API
# ==============================
@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    data = request.get_json(force=True)

    question = data.get("query")
    session_id = data.get("session_id")

    if not question:
        return Response("❌ Empty query", mimetype="text/plain")

    # 🔥 initialize
    initialize_rag()

    chat_history = get_chat_list(session_id)
    rewritten_query = rewrite_query(question, chat_history)

    relevant_chunks, _ = retrieve_chunks(
        rewritten_query, index, stored_chunks, bm25_retriever
    )

    context = "\n\n".join(relevant_chunks)
    history = get_history(session_id)

    answer = chat_with_model(context, question, history)

    def generate():
        for word in answer.split():
            yield word + " "
            time.sleep(0.03)

    add_message(session_id, question, answer)

    return Response(generate(), mimetype="text/plain")


# ==============================
# HEALTH CHECK (VERY IMPORTANT 🔥)
# ==============================
@app.route("/")
def home():
    return "✅ RAG Backend Running!"


# ==============================
# RUN (Railway compatible)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)