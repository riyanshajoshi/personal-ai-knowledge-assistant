import chromadb
from chromadb.utils import embedding_functions
from ingest import load_documents
from chunking import chunk_text

# ChromaDB will use this to auto-embed our text with a local model
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def build_vector_store(folder_path, persist_directory="chroma_db"):
    # Persistent client saves the DB to disk so we don't rebuild it every run
    client = chromadb.PersistentClient(path=persist_directory)

    collection = client.get_or_create_collection(
        name="knowledge_base",
        embedding_function=embedding_fn
    )

    docs = load_documents(folder_path)

    ids = []
    texts = []
    metadatas = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['source']}_{i}"
            ids.append(chunk_id)
            texts.append(chunk)
            metadatas.append({"source": doc["source"], "chunk_id": i})

    # Add everything to the collection (Chroma handles embedding automatically)
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )

    print(f"Added {len(ids)} chunks to the vector store.")
    return collection

def query_vector_store(query, persist_directory="chroma_db", n_results=3):
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_collection(
        name="knowledge_base",
        embedding_function=embedding_fn
    )

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

if __name__ == "__main__":
    build_vector_store("my_knowledge_base")

    # quick test query
    test_query = "What is Artificial Intelligence?"
    results = query_vector_store(test_query)

    print(f"\nTop results for: '{test_query}'\n")
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"Result {i+1} (from {meta['source']}, chunk {meta['chunk_id']}):")
        print(doc[:200] + "...\n")