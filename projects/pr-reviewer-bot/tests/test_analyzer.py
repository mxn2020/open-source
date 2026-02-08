"""Tests for the analyzer module."""

from pr_reviewer_bot.analyzer import ReviewComment, Severity, analyze_diff
from pr_reviewer_bot.diff_parser import DiffFile


def _make_file(filename: str = "test.py", added_lines: list[tuple[int, str]] | None = None):
    return DiffFile(
        filename=filename,
        added_lines=added_lines or [],
        removed_lines=[],
        hunks=[],
    )


class TestLargeChangeRule:
    def test_triggers_above_threshold(self):
        lines = [(i, f"line {i}") for i in range(1, 302)]
        comments = analyze_diff([_make_file(added_lines=lines)])
        large = [c for c in comments if c.rule == "large-change"]
        assert len(large) == 1
        assert large[0].severity == Severity.WARNING

    def test_no_trigger_below_threshold(self):
        lines = [(i, f"line {i}") for i in range(1, 301)]
        comments = analyze_diff([_make_file(added_lines=lines)])
        large = [c for c in comments if c.rule == "large-change"]
        assert len(large) == 0


class TestTodoRule:
    def test_todo_detected(self):
        f = _make_file(added_lines=[(10, "    # TODO: fix this")])
        comments = analyze_diff([f])
        todo = [c for c in comments if c.rule == "todo-comment"]
        assert len(todo) == 1
        assert todo[0].severity == Severity.INFO
        assert "TODO" in todo[0].message

    def test_fixme_detected(self):
        f = _make_file(added_lines=[(5, "    // FIXME: broken")])
        comments = analyze_diff([f])
        todo = [c for c in comments if c.rule == "todo-comment"]
        assert len(todo) == 1
        assert "FIXME" in todo[0].message

    def test_hack_detected(self):
        f = _make_file(added_lines=[(5, "    # HACK: workaround")])
        comments = analyze_diff([f])
        todo = [c for c in comments if c.rule == "todo-comment"]
        assert len(todo) == 1
        assert "HACK" in todo[0].message

    def test_no_todo(self):
        f = _make_file(added_lines=[(1, "    # clean comment")])
        comments = analyze_diff([f])
        todo = [c for c in comments if c.rule == "todo-comment"]
        assert len(todo) == 0


class TestDebugStatementRule:
    def test_console_log(self):
        f = _make_file(
            filename="app.js",
            added_lines=[(1, '    console.log("debug");')],
        )
        comments = analyze_diff([f])
        debug = [c for c in comments if c.rule == "debug-statement"]
        assert len(debug) == 1
        assert debug[0].severity == Severity.WARNING

    def test_print_statement(self):
        f = _make_file(added_lines=[(1, '    print("hello")')])
        comments = analyze_diff([f])
        debug = [c for c in comments if c.rule == "debug-statement"]
        assert len(debug) == 1

    def test_debugger_keyword(self):
        f = _make_file(
            filename="app.js",
            added_lines=[(1, "    debugger;")],
        )
        comments = analyze_diff([f])
        debug = [c for c in comments if c.rule == "debug-statement"]
        assert len(debug) == 1

    def test_no_debug(self):
        f = _make_file(added_lines=[(1, "    x = 1 + 2")])
        comments = analyze_diff([f])
        debug = [c for c in comments if c.rule == "debug-statement"]
        assert len(debug) == 0


class TestHardcodedSecretRule:
    def test_api_key_detected(self):
        f = _make_file(added_lines=[(1, '    API_KEY = "sk-abc123secretkey99"')])
        comments = analyze_diff([f])
        secret = [c for c in comments if c.rule == "hardcoded-secret"]
        assert len(secret) == 1
        assert secret[0].severity == Severity.ERROR

    def test_password_detected(self):
        f = _make_file(added_lines=[(1, '    password = "supersecret123"')])
        comments = analyze_diff([f])
        secret = [c for c in comments if c.rule == "hardcoded-secret"]
        assert len(secret) == 1

    def test_token_detected(self):
        f = _make_file(added_lines=[(1, '    token = "ghp_ABC123longTokenValue456"')])
        comments = analyze_diff([f])
        secret = [c for c in comments if c.rule == "hardcoded-secret"]
        assert len(secret) == 1

    def test_no_secret(self):
        f = _make_file(added_lines=[(1, '    name = "alice"')])
        comments = analyze_diff([f])
        secret = [c for c in comments if c.rule == "hardcoded-secret"]
        assert len(secret) == 0


class TestLongLineRule:
    def test_long_line_detected(self):
        long_content = "x" * 121
        f = _make_file(added_lines=[(1, long_content)])
        comments = analyze_diff([f])
        long = [c for c in comments if c.rule == "long-line"]
        assert len(long) == 1
        assert long[0].severity == Severity.INFO

    def test_normal_line(self):
        f = _make_file(added_lines=[(1, "x" * 120)])
        comments = analyze_diff([f])
        long = [c for c in comments if c.rule == "long-line"]
        assert len(long) == 0


class TestTrailingWhitespaceRule:
    def test_trailing_space(self):
        f = _make_file(added_lines=[(1, "hello   ")])
        comments = analyze_diff([f])
        ws = [c for c in comments if c.rule == "trailing-whitespace"]
        assert len(ws) == 1
        assert ws[0].severity == Severity.INFO

    def test_trailing_tab(self):
        f = _make_file(added_lines=[(1, "hello\t")])
        comments = analyze_diff([f])
        ws = [c for c in comments if c.rule == "trailing-whitespace"]
        assert len(ws) == 1

    def test_no_trailing_whitespace(self):
        f = _make_file(added_lines=[(1, "hello")])
        comments = analyze_diff([f])
        ws = [c for c in comments if c.rule == "trailing-whitespace"]
        assert len(ws) == 0


class TestSeverityFiltering:
    def test_all_severities_present(self):
        f = _make_file(
            added_lines=[
                (1, '    API_KEY = "sk-abc123secretkey99"'),  # error
                (2, '    console.log("test");'),  # warning
                (3, "    # TODO: fix"),  # info
            ]
        )
        comments = analyze_diff([f])
        severities = {c.severity for c in comments}
        assert Severity.ERROR in severities
        assert Severity.WARNING in severities
        assert Severity.INFO in severities
