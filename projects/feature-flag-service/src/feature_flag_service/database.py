"""SQLite-based storage for feature flags."""

import hashlib
import json
import sqlite3
from datetime import datetime, timezone

from .models import (
    EvaluateResponse,
    FeatureFlag,
    FeatureFlagCreate,
    FeatureFlagUpdate,
)


class FlagDatabase:
    """SQLite database for feature flag storage."""

    def __init__(self, db_path: str = "flags.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS flags (
                    id TEXT PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    enabled INTEGER NOT NULL DEFAULT 0,
                    percentage INTEGER NOT NULL DEFAULT 100,
                    tags TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def _row_to_flag(self, row: sqlite3.Row) -> FeatureFlag:
        return FeatureFlag(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            enabled=bool(row["enabled"]),
            percentage=row["percentage"],
            tags=json.loads(row["tags"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def create_flag(self, flag: FeatureFlagCreate) -> FeatureFlag:
        new_flag = FeatureFlag(
            name=flag.name,
            description=flag.description,
            enabled=flag.enabled,
            percentage=flag.percentage,
            tags=flag.tags,
        )
        conn = self._get_conn()
        try:
            conn.execute(
                """
                INSERT INTO flags (id, name, description, enabled, percentage, tags,
                                   created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    new_flag.id,
                    new_flag.name,
                    new_flag.description,
                    int(new_flag.enabled),
                    new_flag.percentage,
                    json.dumps(new_flag.tags),
                    new_flag.created_at.isoformat(),
                    new_flag.updated_at.isoformat(),
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return new_flag

    def get_flag(self, name: str) -> FeatureFlag | None:
        conn = self._get_conn()
        try:
            row = conn.execute("SELECT * FROM flags WHERE name = ?", (name,)).fetchone()
            if row is None:
                return None
            return self._row_to_flag(row)
        finally:
            conn.close()

    def list_flags(self, tag: str | None = None) -> list[FeatureFlag]:
        conn = self._get_conn()
        try:
            rows = conn.execute("SELECT * FROM flags ORDER BY created_at DESC").fetchall()
            flags = [self._row_to_flag(row) for row in rows]
            if tag is not None:
                flags = [f for f in flags if tag in f.tags]
            return flags
        finally:
            conn.close()

    def update_flag(self, name: str, update: FeatureFlagUpdate) -> FeatureFlag | None:
        existing = self.get_flag(name)
        if existing is None:
            return None

        updates = update.model_dump(exclude_none=True)
        if not updates:
            return existing

        if "tags" in updates:
            updates["tags"] = json.dumps(updates["tags"])
        if "enabled" in updates:
            updates["enabled"] = int(updates["enabled"])

        updates["updated_at"] = datetime.now(timezone.utc).isoformat()

        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [name]

        conn = self._get_conn()
        try:
            conn.execute(f"UPDATE flags SET {set_clause} WHERE name = ?", values)
            conn.commit()
        finally:
            conn.close()

        lookup_name = updates.get("name", name)
        return self.get_flag(lookup_name)

    def delete_flag(self, name: str) -> bool:
        conn = self._get_conn()
        try:
            cursor = conn.execute("DELETE FROM flags WHERE name = ?", (name,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def evaluate_flag(self, name: str, user_id: str | None = None) -> EvaluateResponse:
        flag = self.get_flag(name)
        if flag is None:
            return EvaluateResponse(
                flag_name=name,
                enabled=False,
                reason="Flag not found",
            )

        if not flag.enabled:
            return EvaluateResponse(
                flag_name=name,
                enabled=False,
                reason="Flag is disabled",
            )

        if flag.percentage == 100:
            return EvaluateResponse(
                flag_name=name,
                enabled=True,
                reason="Flag is enabled for all users",
            )

        if flag.percentage == 0:
            return EvaluateResponse(
                flag_name=name,
                enabled=False,
                reason="Flag rollout percentage is 0%",
            )

        if user_id is None:
            return EvaluateResponse(
                flag_name=name,
                enabled=True,
                reason=f"Flag is enabled (no user_id for percentage check, {flag.percentage}%)",
            )

        # Consistent percentage bucketing using hash of flag name + user_id
        hash_input = f"{name}:{user_id}"
        hash_val = int(hashlib.sha256(hash_input.encode()).hexdigest(), 16)
        bucket = hash_val % 100

        if bucket < flag.percentage:
            return EvaluateResponse(
                flag_name=name,
                enabled=True,
                reason=f"User is in rollout group ({flag.percentage}%)",
            )
        else:
            return EvaluateResponse(
                flag_name=name,
                enabled=False,
                reason=f"User is outside rollout group ({flag.percentage}%)",
            )
