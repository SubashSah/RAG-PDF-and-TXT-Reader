import shutil
from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from app.enums import ChunkStrategy
from app.services.chunking_service import chunk_documents
from app.services.loader_service import load_document
from app.services.vector_store_service import store_documents
from app.services.document_db_service import save_document_metadata

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunk_strategy: ChunkStrategy = Form(...),
):
    allowed_extensions = {".pdf", ".txt"}

    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported.",
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_document(file_path)

    chunks = chunk_documents(
        documents=documents,
        strategy=chunk_strategy,
    )

    store_documents(chunks)

    save_document_metadata(
        filename=file.filename,
        file_type=suffix,
        chunk_strategy=chunk_strategy.value,
        documents_loaded=len(documents),
        chunks_created=len(chunks),
    )

    return {
        "filename": file.filename,
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
        "preview": chunks[0].page_content[:500],
    }
