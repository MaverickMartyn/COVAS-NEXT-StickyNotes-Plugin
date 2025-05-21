import threading
from threading import Lock
from typing import override
from abc import ABC
import sqlite3

class Note(ABC):
    def __init__(self, note_id: int, content: str, created_at: str):
        self.note_id: int = note_id
        self.content: str = content
        self.created_at: str = created_at

    @override
    def __repr__(self):
        return f"Note(id={self.note_id}, content={self.content}, created_at={self.created_at})"

class NotesStore(ABC):
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.db_conn: sqlite3.Connection | None = None
        # Cache the notes in memory
        self.notes_cache: list[Note] = []
        # Lock for thread-safe access to the database
        self.db_lock: Lock = threading.Lock()

    def initialize_db(self):
        # Initialize the database and create the notes table if it doesn't exist
        self.db_conn = sqlite3.connect(self.db_path, check_same_thread = False)
        with self.db_lock:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.db_conn.commit()

    def get_notes(self) -> list[Note]:
        # Check if notes are already cached
        if self.notes_cache:
            return self.notes_cache

        if self.db_conn is None:
            raise Exception("Database connection is not initialized. Call initialize_db() first.")

        with self.db_lock:
            # Get all notes from the database
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM notes")
            self.notes_cache = cursor.fetchall()

        # Convert to Note objects and cache them
        # self.notes_cache = []
        # self.notes_cache = [cast(Note, row) for row in notes]
        return self.notes_cache

    def add_note(self, content: str) -> int | None:
        if self.db_conn is None:
            raise Exception("Database connection is not initialized. Call initialize_db() first.")

        with self.db_lock:
            # Add a new note to the database
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            self.db_conn.commit()
        
        # Clear the cache if a note is deleted
        self.notes_cache = []
        return cursor.lastrowid
    
    def update_note(self, note_id: int, content: str) -> bool:
        if self.db_conn is None:
            raise Exception("Database connection is not initialized. Call initialize_db() first.")

        with self.db_lock:
            # Update an existing note in the database
            cursor = self.db_conn.cursor()
            cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (content, note_id))
            self.db_conn.commit()
        
        # Clear the cache if a note is deleted
        self.notes_cache = []
        return cursor.rowcount > 0
    
    def delete_note(self, note_id: int) -> bool:
        if self.db_conn is None:
            raise Exception("Database connection is not initialized. Call initialize_db() first.")

        with self.db_lock:
            # Delete a note from the database
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self.db_conn.commit()
        
        # Clear the cache if a note is deleted
        self.notes_cache = []
        return cursor.rowcount > 0
