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
    update_session_title,      # NEW
    get_session_message_count  # NEW
)

from app.memory.db import create_tables

app = Flask(__name__)
CORS(app)

# ==============================
# INIT
# ==============================
create_tables()

documents = load_pdf("data/os_notes.pdf")
chunks = split_text(documents)
index, bm25_retriever, stored_chunks = create_vector_store(chunks)

print("✅ Backend Ready!")


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
    # BUG FIX: also return session title so ChatWindow header can show it
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
    print("Incoming data:", data)

    question = data.get("query")
    session_id = data.get("session_id")

    if not question:
        return jsonify({
            "answer": "❌ Empty query",
            "chunks": [], "scores": [],
            "rewritten_query": "", "session_title": ""
        })

    try:
        chat_history = get_chat_list(session_id)
        rewritten_query = rewrite_query(question, chat_history)

        relevant_chunks, scores = retrieve_chunks(
            rewritten_query, index, stored_chunks, bm25_retriever
        )

        context = "\n\n".join(relevant_chunks)
        history = get_history(session_id)
        answer = chat_with_model(context, question, history)

        add_message(session_id, question, answer)

        # ── Auto-title: set title from first user question ──
        msg_count = get_session_message_count(session_id)
        session_title = ""
        if msg_count == 1:
            # Truncate question to 40 chars for sidebar display
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
            "session_title": session_title   # returned so frontend can update header
        })

    except Exception as e:
        print("ERROR:", str(e))
        import traceback; traceback.print_exc()
        return jsonify({
            "answer": "❌ Backend error",
            "chunks": [], "scores": [],
            "rewritten_query": question,
            "session_title": ""
        })


# ==============================
# STREAMING CHAT
# ==============================
@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    data = request.get_json(force=True)
    question = data.get("query")
    session_id = data.get("session_id")

    if not question:
        return Response("❌ Empty query", mimetype="text/plain")

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

    # Auto-title on first message
    msg_count = get_session_message_count(session_id)
    if msg_count == 1:
        title = question[:40] + ("..." if len(question) > 40 else "")
        update_session_title(session_id, title)

    return Response(generate(), mimetype="text/plain")


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run(debug=True)