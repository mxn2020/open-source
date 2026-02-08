"""Tests for the scanner module."""

import os
import tempfile

from good_first_issue_generator.scanner import CodeOpportunity, scan_directory


def _write_file(directory: str, name: str, content: str) -> str:
    """Helper to write a file in the given directory."""
    path = os.path.join(directory, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return path


class TestScanTodos:
    """Tests for TODO/FIXME/HACK/XXX detection."""

    def test_finds_todo_comment(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "example.py", "# TODO: fix this later\nx = 1\n")
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) >= 1
        assert "TODO" in todos[0].description

    def test_finds_fixme_comment(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "example.py", "x = 1\n# FIXME: broken logic\n")
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) >= 1
        assert "FIXME" in todos[0].description

    def test_finds_hack_comment(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "example.py", "# HACK: workaround for bug\n")
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) >= 1

    def test_finds_xxx_comment(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "example.py", "# XXX: needs review\n")
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) >= 1

    def test_no_false_positive_on_regular_comment(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "example.py", '# This is a regular comment\nx = 1\n')
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) == 0


class TestScanMissingDocstrings:
    """Tests for missing docstring detection."""

    def test_detects_function_without_docstring(self, tmp_path: str) -> None:
        _write_file(
            str(tmp_path),
            "example.py",
            "def my_func():\n    return 1\n",
        )
        results = scan_directory(str(tmp_path))
        docstrings = [r for r in results if r.type == "missing_docstring"]
        assert any("my_func" in d.description for d in docstrings)

    def test_ignores_function_with_docstring(self, tmp_path: str) -> None:
        _write_file(
            str(tmp_path),
            "example.py",
            'def my_func():\n    """Does something."""\n    return 1\n',
        )
        results = scan_directory(str(tmp_path))
        docstrings = [r for r in results if r.type == "missing_docstring"]
        assert not any("my_func" in d.description for d in docstrings)

    def test_detects_class_without_docstring(self, tmp_path: str) -> None:
        _write_file(
            str(tmp_path),
            "example.py",
            "class MyClass:\n    pass\n",
        )
        results = scan_directory(str(tmp_path))
        docstrings = [r for r in results if r.type == "missing_docstring"]
        assert any("MyClass" in d.description for d in docstrings)


class TestScanMissingTypeHints:
    """Tests for missing type hint detection."""

    def test_detects_function_without_return_type(self, tmp_path: str) -> None:
        _write_file(
            str(tmp_path),
            "example.py",
            'def add(a, b):\n    """Add two numbers."""\n    return a + b\n',
        )
        results = scan_directory(str(tmp_path))
        hints = [r for r in results if r.type == "missing_type_hint"]
        assert any("add" in h.description for h in hints)

    def test_ignores_function_with_return_type(self, tmp_path: str) -> None:
        _write_file(
            str(tmp_path),
            "example.py",
            'def add(a: int, b: int) -> int:\n    """Add two numbers."""\n    return a + b\n',
        )
        results = scan_directory(str(tmp_path))
        hints = [r for r in results if r.type == "missing_type_hint"]
        assert not any("add" in h.description for h in hints)


class TestScanMissingTests:
    """Tests for missing test file detection."""

    def test_detects_file_without_test(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "utils.py", "def helper():\n    pass\n")
        results = scan_directory(str(tmp_path))
        missing = [r for r in results if r.type == "missing_test"]
        assert any("utils.py" in m.description for m in missing)

    def test_ignores_file_with_test(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "utils.py", "def helper():\n    pass\n")
        _write_file(str(tmp_path), "test_utils.py", "def test_helper():\n    pass\n")
        results = scan_directory(str(tmp_path))
        missing = [r for r in results if r.type == "missing_test"]
        assert not any("utils.py" in m.description for m in missing)

    def test_ignores_init_files(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "__init__.py", "")
        results = scan_directory(str(tmp_path))
        missing = [r for r in results if r.type == "missing_test"]
        assert not any("__init__" in m.description for m in missing)


class TestScanDirectoryOptions:
    """Tests for scan_directory configuration."""

    def test_custom_extensions(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "app.ts", "// TODO: implement\n")
        _write_file(str(tmp_path), "app.py", "# TODO: implement\n")
        results = scan_directory(str(tmp_path), extensions=[".ts"])
        # Only the .ts file should show a todo
        todos = [r for r in results if r.type == "todo"]
        assert all(t.file.endswith(".ts") for t in todos)

    def test_skips_pycache(self, tmp_path: str) -> None:
        os.makedirs(os.path.join(str(tmp_path), "__pycache__"))
        _write_file(
            str(tmp_path), "__pycache__/cached.py", "# TODO: hidden\n"
        )
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) == 0

    def test_empty_directory(self, tmp_path: str) -> None:
        results = scan_directory(str(tmp_path))
        assert results == []

    def test_opportunity_fields(self, tmp_path: str) -> None:
        _write_file(str(tmp_path), "example.py", "# TODO: check this\n")
        results = scan_directory(str(tmp_path))
        todos = [r for r in results if r.type == "todo"]
        assert len(todos) == 1
        opp = todos[0]
        assert opp.file == "example.py"
        assert opp.line == 1
        assert opp.type == "todo"
        assert opp.difficulty == "easy"
