import streamlit as st
from rag import answer_question

st.set_page_config(page_title="Personal AI Knowledge Assistant", page_icon="🧠")

st.title("🧠 Personal AI Knowledge Assistant")
st.caption("Ask questions about your own notes and documents.")
if st.button("🗑️ Clear conversation"):
    st.session_state.messages = []
    st.rerun()
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
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate and show assistant response
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