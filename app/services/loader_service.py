from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document


def load_document(file_path: Path) -> list[Document]:
    """
    Load a PDF or TXT file and return LangChain Document objects.
    """

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))

    elif suffix == ".txt":
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )

    else:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    return loader.load()