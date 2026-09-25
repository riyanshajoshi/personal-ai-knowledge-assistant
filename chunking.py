def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks of roughly chunk_size characters.
    Overlap helps preserve context across chunk boundaries.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # move forward, but overlap a bit with previous chunk

    return chunks

if __name__ == "__main__":
    from ingest import load_documents

    docs = load_documents("my_knowledge_base")
    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    print(f"Created {len(all_chunks)} chunks from {len(docs)} documents.")
    print("\nSample chunk:")
    print(all_chunks[0])