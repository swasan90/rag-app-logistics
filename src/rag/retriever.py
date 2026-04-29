from langchain_community.vectorstores import OpenSearchVectorSearch

from ..opensearch_client import get_opensearch_client
from ..embeddings import SentenceTransformerEmbeddings
from ..config import OPENSEARCH_INDEX, TOP_K

def get_vectorstore():
    client = get_opensearch_client()
    
    return OpenSearchVectorSearch(
        opensearch_url=None, 
        index_name=OPENSEARCH_INDEX,
        embedding_function=SentenceTransformerEmbeddings(),
        vector_field="embedding",
        text_field="content",
        http_auth=None,
        opensearch_client=client
    )

def get_retriever():
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(
        search_kwargs={
            "k": int(TOP_K or 5),
            "vector_field": "embedding",
            "text_field": "content",
            "metadata_field": "metadata",
        }
    )
    