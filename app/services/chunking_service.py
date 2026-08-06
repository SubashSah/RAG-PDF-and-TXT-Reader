from langchain_core.documents import Document
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

from app.enums import ChunkStrategy


def chunk_documents(
    documents: list[Document],
    strategy: ChunkStrategy,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:
    """
    Split LangChain documents using the selected chunking strategy.
    """

    if strategy == ChunkStrategy.RECURSIVE:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    elif strategy == ChunkStrategy.CHARACTER:

        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    else:
        raise ValueError(
            f"Invalid chunking strategy: {strategy}"
        )

    return splitter.split_documents(documents)