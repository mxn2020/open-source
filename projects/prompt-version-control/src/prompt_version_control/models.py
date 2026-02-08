"""Data models for prompt version control."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class PromptVersion:
    """A single version of a prompt."""

    version: str
    content: str
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    parent_version: str | None = None

    def to_dict(self) -> dict:
        """Convert to a dictionary representation."""
        return {
            "version": self.version,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "parent_version": self.parent_version,
        }


@dataclass
class PromptRecord:
    """A named prompt with its version history."""

    name: str
    description: str = ""
    versions: list[PromptVersion] = field(default_factory=list)
    tags: dict[str, str] = field(default_factory=dict)

    def latest_version(self) -> PromptVersion | None:
        """Return the latest version of the prompt."""
        if not self.versions:
            return None
        return self.versions[-1]

    def get_version(self, version: str) -> PromptVersion | None:
        """Return a specific version of the prompt."""
        for v in self.versions:
            if v.version == version:
                return v
        return None

    def to_dict(self) -> dict:
        """Convert to a dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "versions": [v.to_dict() for v in self.versions],
            "tags": self.tags,
        }
