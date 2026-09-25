import os
from dotenv import load_dotenv
from google import genai
from vectorstore import query_vector_store

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.8-flash"

def answer_question(query, n_results=3):
    # Step 1: Retrieve relevant chunks
    results = query_vector_store(query, n_results=n_results)
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Step 2: Build context from retrieved chunks
    context = "\n\n---\n\n".join(chunks)

    # Step 3: Construct the prompt
    prompt = f"""You are a helpful study assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't have that information in the knowledge base.

Context:
{context}

Question: {query}

Answer:"""

    # Step 4: Call Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text, metadatas

if __name__ == "__main__":
    query = "What is Artificial Intelligence?"
    answer, sources = answer_question(query)

    print(f"Question: {query}\n")
    print(f"Answer: {answer}\n")
    print("Sources used:")
    for meta in sources:
        print(f" - {meta['source']} (chunk {meta['chunk_id']})")