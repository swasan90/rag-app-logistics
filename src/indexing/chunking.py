from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(CHUNK_SIZE),
        chunk_overlap=int(CHUNK_OVERLAP),
        length_function=len,
        is_separator_regex=False
    )
    return splitter.split_text(text)