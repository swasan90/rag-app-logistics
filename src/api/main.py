from fastapi import FastAPI
from pydantic import BaseModel

from ..rag.rag_chain import build_rag_chain

app = FastAPI(title="RAG with OpenSearch and Claude")

rag_chain = build_rag_chain()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    answer = rag_chain.invoke(req.question)
    return AskResponse(answer=answer)
