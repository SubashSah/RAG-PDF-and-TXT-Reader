import sqlite3
from pathlib import Path

DATABASE_PATH = Path("app.db")


def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite database connection.
    """

    return sqlite3.connect(DATABASE_PATH)


def create_document_table() -> None:
    """
    Create the documents table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            chunk_strategy TEXT NOT NULL,
            documents_loaded INTEGER NOT NULL,
            chunks_created INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


create_document_table()


def save_document_metadata(
    filename: str,
    file_type: str,
    chunk_strategy: str,
    documents_loaded: int,
    chunks_created: int,
) -> None:
    """
    Store uploaded document metadata.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents (
            filename,
            file_type,
            chunk_strategy,
            documents_loaded,
            chunks_created
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            filename,
            file_type,
            chunk_strategy,
            documents_loaded,
            chunks_created,
        ),
    )

    connection.commit()
    connection.close()