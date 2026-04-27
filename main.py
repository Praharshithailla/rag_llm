from llm import chat_with_model
from rag.ingest import load_pdf, split_text, create_vector_store
from rag.retrieve import retrieve_chunks
from app.memory.chat_memory import add_message, get_history, get_chat_list
from rag.query_rewrite import rewrite_query 
from app.memory.db import create_tables


# ==============================
# ✅ Step 0: Initialize Database
# ==============================
create_tables()


# ==============================
# 📄 Step 1: Load PDF
# ==============================
documents = load_pdf("data/os_notes.pdf")



chunks = split_text(documents)


index, bm25_retriever, stored_chunks = create_vector_store(chunks)



if __name__ == "__main__":

    print("\n🔥 RAG Chatbot Started (with SQLite Memory + Hybrid Retrieval)\n")

    while True:

        question = input("🧑 You: ")

        
        if question.lower() in ["exit", "quit"]:
            print("👋 Exiting chatbot...")
            break

       
        chat_history = get_chat_list()
        rewritten_query = rewrite_query(question, chat_history)

        print(f"\n[DEBUG] Rewritten Query: {rewritten_query}")

        print("\n[DEBUG] Using HYBRID RETRIEVAL (FAISS + BM25 + RERANK)\n")

        # ==============================
        # 🔍 Step 6: Hybrid Retrieval
        # ==============================
        relevant_chunks = retrieve_chunks(
            rewritten_query,
            index,
            stored_chunks,
            bm25_retriever
        )

        # ==============================
        # 🧾 Step 7: Prepare Context
        # ==============================
        context = "\n\n".join(relevant_chunks)

        # ==============================
        # 🧠 Step 8: Get History for LLM
        # ==============================
        history = get_history()

        # ==============================
        # 🤖 Step 9: Generate Answer
        # ==============================
        answer = chat_with_model(context, question, history)

        # ==============================
        # 📤 Step 10: Print Response
        # ==============================
        print("\n🤖 Bot:\n")
        print(answer)

        # ==============================
        # 💾 Step 11: Store in SQLite
        # ==============================
        add_message(question, answer)