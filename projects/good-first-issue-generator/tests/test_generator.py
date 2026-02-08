"""Tests for the generator module."""

from good_first_issue_generator.generator import IssueTemplate, generate_issues
from good_first_issue_generator.scanner import CodeOpportunity


def _make_opp(
    opp_type: str = "todo",
    file: str = "example.py",
    line: int = 1,
    description: str = "TODO: fix this",
    difficulty: str = "easy",
) -> CodeOpportunity:
    """Helper to create a CodeOpportunity."""
    return CodeOpportunity(
        file=file, line=line, type=opp_type, description=description, difficulty=difficulty
    )


class TestGenerateIssues:
    """Tests for the generate_issues function."""

    def test_generates_issue_from_todo(self) -> None:
        opps = [_make_opp(opp_type="todo", description="TODO: refactor this")]
        issues = generate_issues(opps)
        assert len(issues) == 1
        assert "TODO" in issues[0].title
        assert issues[0].difficulty == "easy"

    def test_generates_issue_from_missing_test(self) -> None:
        opps = [_make_opp(
            opp_type="missing_test",
            description="no test file found for 'utils.py'",
            difficulty="medium",
        )]
        issues = generate_issues(opps)
        assert len(issues) == 1
        assert "tests" in issues[0].title.lower() or "test" in issues[0].title.lower()
        assert "testing" in issues[0].labels

    def test_generates_issue_from_missing_docstring(self) -> None:
        opps = [_make_opp(
            opp_type="missing_docstring",
            description="function 'calculate' is missing a docstring",
        )]
        issues = generate_issues(opps)
        assert len(issues) == 1
        assert "docstring" in issues[0].title.lower()
        assert "documentation" in issues[0].labels

    def test_generates_issue_from_missing_type_hint(self) -> None:
        opps = [_make_opp(
            opp_type="missing_type_hint",
            description="function 'calculate' is missing a return type hint",
            difficulty="medium",
        )]
        issues = generate_issues(opps)
        assert len(issues) == 1
        assert "type hint" in issues[0].title.lower()
        assert "typing" in issues[0].labels

    def test_respects_max_issues(self) -> None:
        opps = [_make_opp(file=f"file{i}.py") for i in range(20)]
        issues = generate_issues(opps, max_issues=5)
        assert len(issues) == 5

    def test_deduplicates_by_title(self) -> None:
        opp = _make_opp()
        issues = generate_issues([opp, opp])
        assert len(issues) == 1

    def test_prioritizes_easy_first(self) -> None:
        opps = [
            _make_opp(difficulty="medium", file="b.py"),
            _make_opp(difficulty="easy", file="a.py"),
        ]
        issues = generate_issues(opps)
        assert issues[0].difficulty == "easy"

    def test_empty_opportunities(self) -> None:
        issues = generate_issues([])
        assert issues == []

    def test_issue_has_labels(self) -> None:
        opps = [_make_opp()]
        issues = generate_issues(opps)
        assert "good first issue" in issues[0].labels

    def test_issue_body_is_nonempty(self) -> None:
        opps = [_make_opp()]
        issues = generate_issues(opps)
        assert len(issues[0].body) > 0
