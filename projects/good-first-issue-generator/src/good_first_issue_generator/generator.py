"""Generator module for converting code opportunities into issue templates."""

from dataclasses import dataclass, field

from good_first_issue_generator.scanner import CodeOpportunity

DIFFICULTY_ORDER = {"easy": 0, "medium": 1}

TYPE_LABELS: dict[str, list[str]] = {
    "todo": ["good first issue", "cleanup"],
    "missing_test": ["good first issue", "testing"],
    "missing_docstring": ["good first issue", "documentation"],
    "missing_type_hint": ["good first issue", "typing"],
}


@dataclass
class IssueTemplate:
    """A generated GitHub issue template."""

    title: str
    body: str
    labels: list[str] = field(default_factory=list)
    difficulty: str = "easy"


def _make_issue(opp: CodeOpportunity) -> IssueTemplate:
    """Convert a single CodeOpportunity into an IssueTemplate."""
    labels = list(TYPE_LABELS.get(opp.type, ["good first issue"]))

    if opp.type == "todo":
        title = f"Remove {opp.description.split(':')[0]} comment in `{opp.file}`"
        body = (
            f"## Description\n\n"
            f"There is a `{opp.description.split(':')[0]}` comment in "
            f"`{opp.file}` at line {opp.line} that should be addressed.\n\n"
            f"**Comment:** {opp.description}\n\n"
            f"## Steps\n\n"
            f"1. Open `{opp.file}` and go to line {opp.line}\n"
            f"2. Read the comment and understand the intended change\n"
            f"3. Implement the change described in the comment\n"
            f"4. Remove the comment once the work is done\n"
            f"5. Add or update tests if applicable\n"
        )
    elif opp.type == "missing_test":
        title = f"Add tests for `{opp.file}`"
        body = (
            f"## Description\n\n"
            f"The file `{opp.file}` does not have a corresponding test file.\n\n"
            f"## Steps\n\n"
            f"1. Create a test file (e.g., `test_{opp.file.split('/')[-1]}`)\n"
            f"2. Write unit tests covering the public functions and classes\n"
            f"3. Aim for meaningful coverage of key code paths\n"
            f"4. Run the test suite to confirm all tests pass\n"
        )
    elif opp.type == "missing_docstring":
        title = f"Add docstring to {opp.description.split("'")[1]} in `{opp.file}`"
        body = (
            f"## Description\n\n"
            f"The {opp.description} in `{opp.file}` at line {opp.line}.\n\n"
            f"## Steps\n\n"
            f"1. Open `{opp.file}` and go to line {opp.line}\n"
            f"2. Add a clear, descriptive docstring explaining purpose, "
            f"parameters, and return values\n"
            f"3. Follow the project's existing docstring conventions\n"
        )
    elif opp.type == "missing_type_hint":
        title = f"Add type hints to {opp.description.split("'")[1]} in `{opp.file}`"
        body = (
            f"## Description\n\n"
            f"The {opp.description} in `{opp.file}` at line {opp.line}.\n\n"
            f"## Steps\n\n"
            f"1. Open `{opp.file}` and go to line {opp.line}\n"
            f"2. Add a return type annotation to the function signature\n"
            f"3. Consider adding parameter type annotations if missing\n"
            f"4. Run the type checker to verify correctness\n"
        )
    else:
        title = f"Address issue in `{opp.file}` at line {opp.line}"
        body = f"## Description\n\n{opp.description}\n"

    return IssueTemplate(title=title, body=body, labels=labels, difficulty=opp.difficulty)


def generate_issues(
    opportunities: list[CodeOpportunity], max_issues: int = 10
) -> list[IssueTemplate]:
    """Generate issue templates from code opportunities.

    Deduplicates by title, prioritizes easy issues first, and limits output count.

    Args:
        opportunities: List of CodeOpportunity objects from the scanner.
        max_issues: Maximum number of issues to generate.

    Returns:
        A list of IssueTemplate objects ready for reporting.
    """
    seen_titles: set[str] = set()
    issues: list[IssueTemplate] = []

    sorted_opps = sorted(
        opportunities, key=lambda o: (DIFFICULTY_ORDER.get(o.difficulty, 99), o.file, o.line)
    )

    for opp in sorted_opps:
        issue = _make_issue(opp)
        if issue.title not in seen_titles:
            seen_titles.add(issue.title)
            issues.append(issue)
        if len(issues) >= max_issues:
            break

    return issues
