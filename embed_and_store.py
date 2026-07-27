from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from pathlib import Path

from ingest_and_chunk import load_documents, chunk_document

DOC_DIR = Path("documents/spark")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "spark_docs"

# 1. Set up embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Set up Chroma client + collection
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)

def build_index():
    docs = load_documents(DOC_DIR)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))

    texts = [c["text"] for c in all_chunks]
    ids = [f'{c["doc_id"]}-{c["chunk_id"]}' for c in all_chunks]
    metadatas = [
        {
            "doc_id": c["doc_id"],
            "chunk_id": c["chunk_id"],
        }
        for c in all_chunks
    ]

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )

def retrieve(query: str, k: int = 5):
    q_emb = model.encode([query])
    result = collection.query(
        query_embeddings=q_emb,
        n_results=k,
    )
    return result  # includes ids, documents, metadatas, distances

if __name__ == "__main__":
    build_index()
    # quick retrieval sanity check
    res = retrieve("How do I create a DataFrame from JSON?")
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        print("----")
        print(meta["doc_id"], meta["chunk_id"], "distance:", dist)
        print(doc[:300])

    print("__________________________Additional retrieval tests__________________________")

    test_queries = [
    "How to programmatically define a schema using StructType and StructField in Spark?",
    "What is a global temporary view and how is it different from a temporary view?",
    "How does Spark SQL cache tables and how to uncache them?",
    "What file formats does Spark natively support and how does it read them?",
    "How to tune spark.sql.shuffle.partitions for a large join?",
    ]

    for q in test_queries:
        print("\n=== QUERY:", q)
        res = retrieve(q, k=5) # top 5 chunks
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            print("----")
            print(meta["doc_id"], "chunk", meta["chunk_id"], "distance:", dist)
            print(doc[:300].replace("\n", " "))