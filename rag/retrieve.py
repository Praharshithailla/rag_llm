from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np

# 🔹 Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔥 Re-ranking model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def retrieve_chunks(question, index, chunks, bm25_retriever, top_k=8):

    # ❌ Prevent crash
    if not question:
        print("❌ Empty question received")
        return [], []

    # =========================
    # 🔹 Step 1: FAISS Retrieval
    # =========================
    query_embedding = embed_model.encode([question])
    distances, indices = index.search(np.array(query_embedding), top_k)

    faiss_results = [chunks[i]["text"] for i in indices[0]]

    # =========================
    # 🔹 Step 2: BM25 Retrieval
    # =========================
    bm25_docs = list(bm25_retriever.invoke(question))
    bm25_results = [doc.page_content for doc in bm25_docs]

    # =========================
    # 🔥 Step 3: Hybrid Merge (RRF)
    # =========================
    scores_dict = {}

    for rank, text in enumerate(bm25_results):
        scores_dict[text] = scores_dict.get(text, 0) + (1 / (rank + 1))

    for rank, text in enumerate(faiss_results):
        scores_dict[text] = scores_dict.get(text, 0) + (1 / (rank + 1))

    sorted_docs = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)

    candidates = [doc for doc, _ in sorted_docs[:top_k]]

    # =========================
    # 🔥 Step 4: RE-RANKING
    # =========================
    pairs = [[question, doc] for doc in candidates]

    rerank_scores = reranker.predict(pairs)

    reranked = list(zip(candidates, rerank_scores))
    reranked = sorted(reranked, key=lambda x: x[1], reverse=True)

    # =========================
    # 🔹 Step 5: Final Results + Scores
    # =========================
    results = []
    final_scores = []

    for text, score in reranked[:3]:
        for chunk in chunks:
            if chunk["text"] == text:
                results.append(
                    f"{chunk['text']}\n(Source: {chunk['source']})"
                )
                final_scores.append(float(score))  # 🔥 IMPORTANT
                break

    # =========================
    # 🔍 DEBUG
    # =========================
    print("\n[DEBUG] AFTER RERANKING:\n")
    for text, score in reranked[:3]:
        print(f"Score: {score:.4f}")
        print(text[:200], "\n---")

    return results, final_scores