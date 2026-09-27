# 🧠 Personal AI Knowledge Assistant

🔗 **[Try the live demo](https://personal-ai-knowledge-assistant-wub39unimxgemyyr6h24ng.streamlit.app/)** — runs on sample CS fundamentals content; clone the repo to use it with your own documents

A conversational RAG (Retrieval-Augmented Generation) system that lets you chat with your own notes and documents — PDFs, PowerPoints, and text/markdown files — instead of manually searching through them.

Ask a question in plain English, and the assistant retrieves the most relevant passages from your knowledge base and generates a grounded, source-attributed answer using Google's Gemini API.

## Demo

> Ask: *"What is a process in an operating system?"*
> Answer: *"A process is a program in execution. Each process has its own memory space, unlike threads which share memory within a process."*
> Sources: `os_notes.md`

Every answer includes exactly which document(s) it was generated from — no black-box responses.

## How it works

This isn't just "call an LLM" — it's a full retrieval pipeline:

1. **Ingestion** (`ingest.py`) — Loads documents from a folder, supporting `.pdf`, `.pptx`, `.txt`, and `.md` files, and extracts their raw text.
2. **Chunking** (`chunking.py`) — Splits long documents into overlapping ~500-character chunks, so retrieval stays precise and no idea gets cut off at a boundary.
3. **Embedding & Vector Storage** (`vectorstore.py`) — Converts each chunk into a vector embedding (via a local `sentence-transformers` model, no API cost) and stores it in a persistent **ChromaDB** vector database.
4. **Retrieval + Relevance Filtering** (`rag.py`) — For a given question, retrieves the closest-matching chunks by semantic similarity, then filters out anything below a relevance threshold — so answers aren't padded with irrelevant "closest available" content when a topic only appears in one document.
5. **Generation** (`rag.py`) — Passes the filtered, relevant chunks as context to Google's Gemini API, which generates a natural-language answer *grounded in the retrieved content* rather than the model's own training data.
6. **Chat Interface** (`app.py`) — A Streamlit-based chat UI with conversation history and an expandable "Sources used" section per answer.

## Tech Stack

| Component | Tool |
|---|---|
| Language | Python |
| Document parsing | `pypdf`, `python-pptx` |
| Embeddings | `sentence-transformers` (local, free) |
| Vector database | `ChromaDB` |
| LLM | Google Gemini API (`google-genai`) |
| UI | Streamlit |

## Design decisions worth noting

- **Relevance filtering, not just top-k retrieval:** Early testing showed that always returning the top 5 chunks caused irrelevant documents to appear in the source list when a query only matched one document well. Instead of a fixed count, chunks are filtered by a distance threshold determined empirically by comparing distance scores for genuinely relevant vs. irrelevant matches.
- **Local embeddings:** Embedding generation runs entirely on-device via `sentence-transformers`, keeping personal document content from being sent anywhere just to generate embeddings — only the final retrieved snippets are sent to the LLM API for answer generation.
- **Retry logic for LLM calls:** Handles transient API unavailability (e.g. `503` errors during high demand) with exponential backoff, rather than failing outright.
- **Privacy by design:** Personal documents and the local vector database are excluded from version control (see `.gitignore`) — this repo ships as a *tool*, not with anyone's actual data baked in.

## Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd personal-ai-knowledge-assistant

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install pypdf python-pptx chromadb sentence-transformers google-genai streamlit python-dotenv

# Add your Gemini API key
echo GEMINI_API_KEY=your-key-here > .env
```

Get a free API key at [aistudio.google.com](https://aistudio.google.com).

## Usage

1. Drop your documents (`.pdf`, `.pptx`, `.txt`, `.md`) into a `my_knowledge_base/` folder.
2. Build the vector store:
   ```bash
   python vectorstore.py
   ```
3. Launch the chat interface:
   ```bash
   streamlit run app.py
   ```
4. Ask questions about your documents in the browser.

## Roadmap

This is a v1 focused on proving the core architecture end-to-end. Planned next steps:

- Support for additional file types (emails, exported chat logs, OCR for scanned/image-based documents)
- Persistent conversation memory across sessions
- Fully local/offline mode using a local LLM (e.g. via Ollama) instead of an external API, for complete data privacy
- Incremental ingestion (add new documents without rebuilding the entire vector store)
- Authentication, if ever deployed beyond local use

## Why this project

Built to explore practical, production-relevant RAG system design — not just calling an LLM API, but the surrounding engineering: chunking strategy, vector search, relevance tuning, and grounding answers in real source material with transparent attribution.