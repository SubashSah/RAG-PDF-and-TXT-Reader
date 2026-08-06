import sqlite3
from pathlib import Path

DATABASE_PATH = Path("app.db")


def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite database connection.
    """

    return sqlite3.connect(DATABASE_PATH)


def create_booking_table() -> None:
    """
    Create the bookings table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            interview_date TEXT NOT NULL,
            interview_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


create_booking_table()


def save_booking(
    name: str,
    email: str,
    date: str,
    time: str,
) -> None:
    """
    Store a completed booking.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bookings (
            name,
            email,
            interview_date,
            interview_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            date,
            time,
        ),
    )

    connection.commit()
    connection.close()