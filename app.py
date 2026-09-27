import streamlit as st
import chromadb
from ingest import get_active_knowledge_base_path
from rag import answer_question

st.set_page_config(page_title="Personal AI Knowledge Assistant", page_icon="🧠")

st.title("🧠 Personal AI Knowledge Assistant")
st.caption("Ask questions about your own notes and documents.")

if st.button("🗑️ Clear conversation"):
    st.session_state.messages = []
    st.rerun()

# Determine which knowledge base is active (personal or sample fallback)
kb_path = get_active_knowledge_base_path()
using_sample_data = kb_path == "sample_docs"

if using_sample_data:
    st.info(
        "📂 Currently using **sample CS fundamentals content** for this demo. "
        "Clone the repo and drop your own files into `my_knowledge_base/` to use your personal documents."
    )

# Ensure the vector store exists (builds it on first run, e.g. on a fresh deploy)
def vector_store_exists(persist_directory="chroma_db"):
    try:
        client = chromadb.PersistentClient(path=persist_directory)
        client.get_collection(name="knowledge_base")
        return True
    except Exception:
        return False

if not vector_store_exists():
    with st.spinner("Setting up knowledge base for the first time... this may take a minute."):
        from vectorstore import build_vector_store
        build_vector_store(kb_path)

# Keep chat history across interactions
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("Sources used"):
                for src in msg["sources"]:
                    st.write(f"- {src['source']} (chunk {src['chunk_id']})")

# Chat input box
if query := st.chat_input("Ask something about your knowledge base..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching your knowledge base..."):
            answer, sources = answer_question(query)
        st.markdown(answer)
        with st.expander("Sources used"):
            for src in sources:
                st.write(f"- {src['source']} (chunk {src['chunk_id']})")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })