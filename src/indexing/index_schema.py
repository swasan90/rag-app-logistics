from opensearchpy import OpenSearchException
from ..config import OPENSEARCH_INDEX
from ..opensearch_client import get_opensearch_client
from ..embeddings import get_embedding_model

def create_index_if_not_exists():
    client = get_opensearch_client()
    if client.indices.exists(index=OPENSEARCH_INDEX):
        print(f"Index {OPENSEARCH_INDEX} already exists")
        return 
    dimensions = get_embedding_model().get_sentence_embedding_dimension()
    print(f"Creating index {OPENSEARCH_INDEX} with dimensions {dimensions}")

    body={
        "settings": {
            "index":{
                "knn": True
            }
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text"
                },
                "metadata": {
                    "type": "object",
                    "enabled": True                     
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": dimensions,
                    "method": {
                        "name": "hnsw",
                        "engine": "faiss",
                        "space_type": "cosinesimil"
                    }
                }
            }
        }
    }

    try:
        client.indices.create(index=OPENSEARCH_INDEX, body=body)
        print(f"Index {OPENSEARCH_INDEX} created successfully")
    except OpenSearchException as e:
        print(f"Error creating index {OPENSEARCH_INDEX}: {e}")
        raise e
