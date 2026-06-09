from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOC_DIR = Path("documents/spark")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""],  # paragraph, line, word, fallback
)

def load_documents(doc_dir: Path):
    docs = []
    for path in doc_dir.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        docs.append({"id": path.name, "path": str(path), "text": text})
    return docs

def chunk_document(doc):
    chunks = text_splitter.split_text(doc["text"])
    return [
        {
            "doc_id": doc["id"],
            "chunk_id": i,
            "text": chunk,
        }
        for i, chunk in enumerate(chunks)
    ]

def main():
    docs = load_documents(DOC_DIR)
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))

    print(f"Loaded {len(docs)} documents") # 12 documents
    print(f"Generated {len(all_chunks)} chunks") # 258 chunks

    # print a few sample chunks
    for c in all_chunks[:5]:
        print("-" * 40)
        print(c["doc_id"], "chunk", c["chunk_id"])
        print(c["text"][:300])

if __name__ == "__main__":
    main()