from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .retriever import get_retriever
from .llm_claude import get_claude_llm

SYSTEM_PROMPT = """You are a helpful assistant answering questions using the provided context.
Use ONLY the context to answer. If the answer is not in the context, say you don't know.

Context:
{context}
"""

USER_PROMPT = """Question: {question}"""

def format_docs(docs):
    return "\n\n".join(f"[{i+1}] {d.page_content}" for i, d in enumerate(docs))

def build_rag_chain():
    retriever = get_retriever()
    llm = get_claude_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT),
        ]
    )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
