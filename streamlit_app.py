import requests
import streamlit as st


st.set_page_config(page_title="RAG Assistant", page_icon=":books:", layout="centered")
st.title("RAG Assistant")
st.caption("Ask questions against your indexed documents.")

if "history" not in st.session_state:
    st.session_state.history = []

api_url = st.sidebar.text_input("API URL", "http://127.0.0.1:8000/ask").strip()
timeout_seconds = st.sidebar.slider("Request timeout (seconds)", min_value=10, max_value=120, value=45)
if st.sidebar.button("Clear conversation", use_container_width=True):
    st.session_state.history = []
    st.rerun()

question = st.text_area("Question", placeholder="Ask a question about your indexed documents...", height=120)
ask_clicked = st.button("Ask", type="primary", use_container_width=True)

if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(
                    api_url,
                    json={"question": question.strip()},
                    timeout=timeout_seconds,
                )
                response.raise_for_status()
                payload = response.json()
                answer = payload.get("answer", "")
                st.session_state.history.append(
                    {"question": question.strip(), "answer": answer}
                )
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
            except ValueError:
                st.error("The API did not return valid JSON.")

if st.session_state.history:
    st.subheader("Conversation")
    for item in reversed(st.session_state.history):
        st.markdown(f"**Question:** {item['question']}")
        st.markdown(f"**Answer:** {item['answer']}")
        st.divider()
