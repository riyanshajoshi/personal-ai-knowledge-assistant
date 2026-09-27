import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError
from vectorstore import query_vector_store

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.8-flash"

def call_gemini_with_retry(prompt, max_retries=4):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
        except ServerError as e:
            wait = 2 ** attempt  # 1s, 2s, 4s, 8s
            print(f"Server busy, retrying in {wait}s... (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
    raise RuntimeError("Gemini API unavailable after retries. Please try again in a moment.")

def answer_question(query, n_results=5, max_distance=0.5):
    results = query_vector_store(query, n_results=n_results)
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]


    # Keep only chunks that are genuinely close matches
    filtered = [
        (chunk, meta) for chunk, meta, dist in zip(chunks, metadatas, distances)
        if dist <= max_distance
    ]

    if not filtered:
        return "I don't have that information in the knowledge base.", []

    chunks = [c for c, m in filtered]
    metadatas = [m for c, m in filtered]

    context = "\n\n---\n\n".join(chunks)

    prompt = f"""You are a helpful study assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't have that information in the knowledge base.

Context:
{context}

Question: {query}

Answer:"""

    response = call_gemini_with_retry(prompt)
    return response.text, metadatas

if __name__ == "__main__":
    query = "What is a process?"
    answer, sources = answer_question(query)

    print(f"Question: {query}\n")
    print(f"Answer: {answer}\n")
    print("Sources used:")
    for meta in sources:
        print(f" - {meta['source']} (chunk {meta['chunk_id']})")