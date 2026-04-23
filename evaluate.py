from test_data import test_data
from rag.retrieve import retrieve_chunks
from rag.ingest import load_pdf, split_text, create_vector_store

# Load system
documents = load_pdf("data/os_notes.pdf")
chunks = split_text(documents)
index, bm25_retriever, stored_chunks = create_vector_store(chunks)


def evaluate():

    recall_hits = 0
    mrr_total = 0

    for item in test_data:

        question = item["question"]
        keyword = item["answer_keyword"]

        results = retrieve_chunks(
            question,
            index,
            stored_chunks,
            bm25_retriever
        )

        found = False

        for rank, chunk in enumerate(results, start=1):

            if keyword.lower() in chunk.lower():
                recall_hits += 1
                mrr_total += (1 / rank)
                found = True
                break

        if not found:
            mrr_total += 0

    total = len(test_data)

    recall = recall_hits / total
    mrr = mrr_total / total

    print("\n===== EVALUATION RESULTS =====")
    print(f"Recall@K: {recall:.2f}")
    print(f"MRR: {mrr:.2f}")


if __name__ == "__main__":
    evaluate()