"""SQLite-backed storage for prompt versions."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from prompt_version_control.models import PromptVersion


class PromptStore:
    """Manages prompt version storage using SQLite."""

    def __init__(self, db_path: str = ".prompts.db") -> None:
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the database tables if they don't exist."""
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS prompts (
                name TEXT PRIMARY KEY,
                description TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                parent_version TEXT,
                FOREIGN KEY (name) REFERENCES prompts(name) ON DELETE CASCADE,
                UNIQUE(name, version)
            );
            CREATE TABLE IF NOT EXISTS tags (
                name TEXT NOT NULL,
                tag TEXT NOT NULL,
                version TEXT NOT NULL,
                PRIMARY KEY (name, tag),
                FOREIGN KEY (name) REFERENCES prompts(name) ON DELETE CASCADE
            );
            """)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.commit()

    def _row_to_version(self, row: sqlite3.Row) -> PromptVersion:
        """Convert a database row to a PromptVersion."""
        return PromptVersion(
            version=row["version"],
            content=row["content"],
            metadata=json.loads(row["metadata"]),
            created_at=row["created_at"],
            parent_version=row["parent_version"],
        )

    def save(self, name: str, content: str, metadata: dict | None = None) -> PromptVersion:
        """Save a new version of a prompt, auto-incrementing the version number."""
        metadata = metadata or {}

        # Ensure the prompt record exists
        self._conn.execute(
            "INSERT OR IGNORE INTO prompts (name) VALUES (?)",
            (name,),
        )

        # Determine the next version number
        row = self._conn.execute(
            "SELECT version FROM versions WHERE name = ? ORDER BY id DESC LIMIT 1",
            (name,),
        ).fetchone()

        if row is None:
            next_version = "1.0"
            parent_version = None
        else:
            current = row["version"]
            major = int(current.split(".")[0])
            next_version = f"{major + 1}.0"
            parent_version = current

        created_at = datetime.now(timezone.utc).isoformat()

        self._conn.execute(
            """INSERT INTO versions (name, version, content, metadata, created_at, parent_version)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, next_version, content, json.dumps(metadata), created_at, parent_version),
        )
        self._conn.commit()

        return PromptVersion(
            version=next_version,
            content=content,
            metadata=metadata,
            created_at=created_at,
            parent_version=parent_version,
        )

    def get(self, name: str, version: str | None = None) -> PromptVersion | None:
        """Get a specific version or the latest version of a prompt."""
        if version:
            row = self._conn.execute(
                "SELECT * FROM versions WHERE name = ? AND version = ?",
                (name, version),
            ).fetchone()
        else:
            row = self._conn.execute(
                "SELECT * FROM versions WHERE name = ? ORDER BY id DESC LIMIT 1",
                (name,),
            ).fetchone()

        if row is None:
            return None
        return self._row_to_version(row)

    def list_prompts(self) -> list[str]:
        """List all prompt names."""
        rows = self._conn.execute("SELECT name FROM prompts ORDER BY name").fetchall()
        return [row["name"] for row in rows]

    def list_versions(self, name: str) -> list[PromptVersion]:
        """List all versions of a prompt."""
        rows = self._conn.execute(
            "SELECT * FROM versions WHERE name = ? ORDER BY id ASC",
            (name,),
        ).fetchall()
        return [self._row_to_version(row) for row in rows]

    def tag(self, name: str, version: str, tag_name: str) -> None:
        """Tag a specific version of a prompt."""
        # Verify the version exists
        row = self._conn.execute(
            "SELECT version FROM versions WHERE name = ? AND version = ?",
            (name, version),
        ).fetchone()
        if row is None:
            raise ValueError(f"Version {version} of prompt '{name}' not found")

        self._conn.execute(
            "INSERT OR REPLACE INTO tags (name, tag, version) VALUES (?, ?, ?)",
            (name, tag_name, version),
        )
        self._conn.commit()

    def get_by_tag(self, name: str, tag_name: str) -> PromptVersion | None:
        """Get a prompt version by its tag."""
        row = self._conn.execute(
            "SELECT version FROM tags WHERE name = ? AND tag = ?",
            (name, tag_name),
        ).fetchone()
        if row is None:
            return None
        return self.get(name, row["version"])

    def delete(self, name: str) -> bool:
        """Delete all versions of a prompt. Returns True if the prompt existed."""
        row = self._conn.execute("SELECT name FROM prompts WHERE name = ?", (name,)).fetchone()
        if row is None:
            return False

        self._conn.execute("DELETE FROM tags WHERE name = ?", (name,))
        self._conn.execute("DELETE FROM versions WHERE name = ?", (name,))
        self._conn.execute("DELETE FROM prompts WHERE name = ?", (name,))
        self._conn.commit()
        return True

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
