from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 📄 Step 1: Load PDF
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents


# ✂️ Step 2: Split text into chunks
def split_text(documents, chunk_size=600, chunk_overlap=100):

    chunks = []

    for doc in documents:
        text = doc.page_content
        page = doc.metadata.get("page", "unknown")

        start = 0

        while start < len(text):
            chunk_text = text[start:start + chunk_size]

            chunks.append({
                "text": chunk_text,
                "source": f"OS_notes.pdf page {page+1}"
            })

            start += chunk_size - chunk_overlap

    return chunks


# 🧠 Step 3: Create FAISS + BM25
def create_vector_store(chunks):

    texts = [chunk["text"] for chunk in chunks]

    # 🔹 FAISS embeddings
    embeddings = model.encode(texts)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # 🔥 BM25 setup (NEW API compatible)
    documents = [Document(page_content=chunk["text"]) for chunk in chunks]
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 5

    print(f"\n[INFO] Total chunks stored: {len(chunks)}")

    return index, bm25_retriever, chunks