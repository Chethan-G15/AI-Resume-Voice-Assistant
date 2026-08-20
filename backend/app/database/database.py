import sqlite3
from pathlib import Path


# Find the project root folder that is AI-Resume-Voice-Agent
BASE_DIR = Path(__file__).resolve().parents[3]

# Database folder find database folder inside root folder
DATABASE_DIR = BASE_DIR / "database"

# Create database folder if it doesn't exist
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database file
DATABASE_PATH = DATABASE_DIR / "resumes.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def create_tables():
    """
    Create the resumes table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # Create table for new installations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            career_objective TEXT,
            skills TEXT,
            education TEXT,
            experience TEXT,
            projects TEXT,
            certifications TEXT
        )
    """)

    # Safely add new columns to an existing database
    cursor.execute("PRAGMA table_info(resumes)")
    columns = [column[1] for column in cursor.fetchall()]

    if "email" not in columns:
        cursor.execute("ALTER TABLE resumes ADD COLUMN email TEXT")

    if "phone" not in columns:
        cursor.execute("ALTER TABLE resumes ADD COLUMN phone TEXT")

    connection.commit()

    connection.close()