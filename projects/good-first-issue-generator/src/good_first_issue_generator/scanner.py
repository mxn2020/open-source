"""Scanner module for finding code improvement opportunities in a project directory."""

import os
import re
from dataclasses import dataclass

SKIP_DIRS = {"node_modules", "__pycache__", ".git", "venv", ".venv", "dist"}
DEFAULT_EXTENSIONS = [".py", ".ts", ".js"]

TODO_PATTERN = re.compile(r"(?:#|//)\s*(TODO|FIXME|HACK|XXX)\b[:\s]*(.*)", re.IGNORECASE)

DEF_PATTERN = re.compile(r"^\s*def\s+(\w+)\s*\(")
CLASS_PATTERN = re.compile(r"^\s*class\s+(\w+)\s*[\(:]")
DOCSTRING_OPENERS = ('"""', "'''", 'r"""', "r'''")

TYPE_HINT_PATTERN = re.compile(r"^\s*def\s+\w+\s*\(.*\)\s*:")


@dataclass
class CodeOpportunity:
    """Represents a single code improvement opportunity."""

    file: str
    line: int
    type: str  # "todo", "missing_test", "missing_docstring", "missing_type_hint"
    description: str
    difficulty: str  # "easy", "medium"


def _iter_source_files(
    path: str, extensions: list[str]
) -> list[str]:
    """Walk the directory tree and yield source file paths, skipping common dirs."""
    results: list[str] = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if any(fname.endswith(ext) for ext in extensions):
                results.append(os.path.join(root, fname))
    return results


def _find_todos(filepath: str, lines: list[str]) -> list[CodeOpportunity]:
    """Find TODO/FIXME/HACK/XXX comments in a file."""
    opportunities: list[CodeOpportunity] = []
    for i, line in enumerate(lines, start=1):
        match = TODO_PATTERN.search(line)
        if match:
            tag = match.group(1).upper()
            message = match.group(2).strip() or "no description"
            opportunities.append(
                CodeOpportunity(
                    file=filepath,
                    line=i,
                    type="todo",
                    description=f"{tag}: {message}",
                    difficulty="easy",
                )
            )
    return opportunities


def _find_missing_docstrings(filepath: str, lines: list[str]) -> list[CodeOpportunity]:
    """Find functions and classes without docstrings in Python files."""
    if not filepath.endswith(".py"):
        return []
    opportunities: list[CodeOpportunity] = []
    for i, line in enumerate(lines):
        def_match = DEF_PATTERN.match(line)
        class_match = CLASS_PATTERN.match(line)
        name = None
        kind = ""
        if def_match:
            name = def_match.group(1)
            kind = "function"
        elif class_match:
            name = class_match.group(1)
            kind = "class"

        if name is None:
            continue

        # Check if the next non-empty line is a docstring
        has_docstring = False
        for j in range(i + 1, min(i + 5, len(lines))):
            stripped = lines[j].strip()
            if not stripped:
                continue
            if any(stripped.startswith(opener) for opener in DOCSTRING_OPENERS):
                has_docstring = True
            break

        if not has_docstring:
            opportunities.append(
                CodeOpportunity(
                    file=filepath,
                    line=i + 1,
                    type="missing_docstring",
                    description=f"{kind} '{name}' is missing a docstring",
                    difficulty="easy",
                )
            )
    return opportunities


def _find_missing_type_hints(filepath: str, lines: list[str]) -> list[CodeOpportunity]:
    """Find function definitions without return type hints in Python files."""
    if not filepath.endswith(".py"):
        return []
    opportunities: list[CodeOpportunity] = []
    for i, line in enumerate(lines, start=1):
        def_match = DEF_PATTERN.match(line)
        if def_match and "->" not in line:
            name = def_match.group(1)
            opportunities.append(
                CodeOpportunity(
                    file=filepath,
                    line=i,
                    type="missing_type_hint",
                    description=f"function '{name}' is missing a return type hint",
                    difficulty="medium",
                )
            )
    return opportunities


def _find_missing_tests(
    source_files: list[str], base_path: str
) -> list[CodeOpportunity]:
    """Find source files that do not have corresponding test files."""
    opportunities: list[CodeOpportunity] = []
    test_basenames: set[str] = set()
    src_files_to_check: list[str] = []

    for fpath in source_files:
        basename = os.path.basename(fpath)
        if basename.startswith("test_") or basename.endswith("_test.py"):
            test_basenames.add(basename)
        elif basename.endswith(".py") and basename != "__init__.py":
            src_files_to_check.append(fpath)

    for fpath in src_files_to_check:
        basename = os.path.basename(fpath)
        stem = basename.removesuffix(".py")
        expected_test = f"test_{stem}.py"
        alt_test = f"{stem}_test.py"
        if expected_test not in test_basenames and alt_test not in test_basenames:
            rel_path = os.path.relpath(fpath, base_path)
            opportunities.append(
                CodeOpportunity(
                    file=rel_path,
                    line=1,
                    type="missing_test",
                    description=f"no test file found for '{basename}'",
                    difficulty="medium",
                )
            )
    return opportunities


def scan_directory(
    path: str, extensions: list[str] | None = None
) -> list[CodeOpportunity]:
    """Scan a project directory for code improvement opportunities.

    Args:
        path: Root directory to scan.
        extensions: File extensions to include. Defaults to .py, .ts, .js.

    Returns:
        A list of CodeOpportunity objects describing found opportunities.
    """
    if extensions is None:
        extensions = DEFAULT_EXTENSIONS

    abs_path = os.path.abspath(path)
    source_files = _iter_source_files(abs_path, extensions)
    opportunities: list[CodeOpportunity] = []

    for filepath in source_files:
        rel_path = os.path.relpath(filepath, abs_path)
        try:
            with open(filepath, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue

        opportunities.extend(_find_todos(rel_path, lines))
        opportunities.extend(_find_missing_docstrings(rel_path, lines))
        opportunities.extend(_find_missing_type_hints(rel_path, lines))

    opportunities.extend(_find_missing_tests(source_files, abs_path))

    return opportunities
