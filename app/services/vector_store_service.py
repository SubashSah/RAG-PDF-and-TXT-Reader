import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

COLLECTION_NAME = "documents"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
)

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=os.getenv("QDRANT_PORT"),
)


def _create_collection_if_not_exists() -> None:
    """
    Create the Qdrant collection if it does not already exist.
    """

    collections = client.get_collections().collections

    existing = {collection.name for collection in collections}

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


_create_collection_if_not_exists()


vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)


def store_documents(
    documents: list[Document],
) -> None:
    """
    Generate embeddings and store documents in Qdrant.
    """

    vector_store.add_documents(documents)


retriever = vector_store.as_retriever(search_kwargs={"k": 4})


def retrieve_documents(
    query: str,
) -> list[Document]:
    """
    Retrieve documents from Qdrant based on a query.
    """
    points_count = client.count(collection_name=COLLECTION_NAME, exact=True).count

    if points_count == 0:
        return []

    return retriever.invoke(query)
