import os
import glob
from uuid import uuid4

from ..config import OPENSEARCH_INDEX
from ..opensearch_client import get_opensearch_client
from ..embeddings import SentenceTransformerEmbeddings
from .chunking import chunk_text
from .index_schema import create_index_if_not_exists

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "sample_docs")

def load_files():
    patterns = ["*.md", "*.txt"]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(DATA_DIR, pattern)))
    return files

def index_documents():
    create_index_if_not_exists()
    client = get_opensearch_client()
    embeddings = SentenceTransformerEmbeddings()

    files = load_files()
    print(f"Found {len(files)} files")

    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        print(f"Indexing {len(chunks)} chunks from {os.path.basename(path)}")

        chunk_embeddings = embeddings.embed_documents(chunks)
        actions = []
        for chunk, embedding in zip(chunks, chunk_embeddings):
            doc_id = str(uuid4())
            body = {
                "content": chunk,
                "metadata": {
                    "source": os.path.basename(path)
                },
                "embedding": embedding,
            }
            actions.append(
                {
                    "_op_type": "index",
                    "_index": OPENSEARCH_INDEX,
                    "_id": doc_id,
                    "_source": body,
                }
            )

        # bulk index
        from opensearchpy.helpers import bulk
        bulk(client, actions)
        print(f"Indexed {len(chunks)} chunks from {os.path.basename(path)}")

if __name__ == "__main__":
    index_documents()
