"""Generate the deterministic requirement-to-test traceability matrix.

Repository maintenance tooling, not runtime behaviour. Scans ``tests/`` for
``# verifies: <FAMILY>-<nn>`` markers and ``agent-runs/**/implementer-prompt*.md``
for requirement definitions; writes ``docs/TRACEABILITY.md``. Wire a staleness
test once the project has a suite: regenerate to a temp path and byte-compare
against the committed file, failing with a "regenerate and commit" message.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_RELATIVE_PATH = Path("docs/TRACEABILITY.md")

MARKER_RE = re.compile(r"^\s*#\s*verifies:\s*(?P<family>[A-Z][A-Z0-9]*)-(?P<number>\d+)\b")
CANONICAL_REQUIREMENT_RE = re.compile(r"\*\*(?P<family>[A-Z][A-Z0-9]*)-(?P<number>\d+)\s+—\s+(?P<title>.*?)\*\*")
BRACKET_REQUIREMENT_RE = re.compile(r"\[(?P<family>[A-Z][A-Z0-9]*)-(?P<start>\d+)(?:\.\.(?P<end>\d+))?\]")
SECTION_HEADING_RE = re.compile(r"^\s*(?:\d+\.|[-*])\s+\*\*(?P<title>.+?)\*\*")
DIRECT_BRACKET_RE = re.compile(r"^\s*[-*]\s+\[[A-Z][A-Z0-9]*-\d+(?:\.\.\d+)?\]\s+(?P<title>.+)$")


@dataclass(frozen=True, order=True)
class RequirementId:
    """A stable requirement ID split into deterministic sort fields."""

    family: str
    number: int

    @property
    def label(self) -> str:
        return f"{self.family}-{self.number:02d}"


@dataclass(frozen=True)
class Definition:
    """One requirement definition discovered in an implementer prompt."""

    requirement_id: RequirementId
    title: str
    source_path: str
    line: int
    priority: int


@dataclass(frozen=True, order=True)
class TestReference:
    """A test function carrying a requirement marker."""

    path: str
    name: str
    line: int


def _normalise_title(value: str) -> str:
    return " ".join(value.strip().strip(".:").split())


def _requirement_id(match: re.Match[str]) -> RequirementId:
    return RequirementId(family=match["family"], number=int(match["number"]))


def _bracket_requirement_ids(match: re.Match[str]) -> tuple[RequirementId, ...]:
    start = int(match["start"])
    end = int(match["end"] or start)
    if end < start:
        return ()
    return tuple(RequirementId(family=match["family"], number=number) for number in range(start, end + 1))


def _relative_path(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _record_definition(definitions: dict[RequirementId, Definition], candidate: Definition) -> None:
    """Keep the most specific definition, deterministically on ties."""

    current = definitions.get(candidate.requirement_id)
    if current is None:
        definitions[candidate.requirement_id] = candidate
        return
    if candidate.priority > current.priority:
        definitions[candidate.requirement_id] = candidate
        return
    if candidate.priority == current.priority and (candidate.source_path, candidate.line) < (
        current.source_path,
        current.line,
    ):
        definitions[candidate.requirement_id] = candidate


def _prompt_files(repo_root: Path) -> tuple[Path, ...]:
    return tuple(sorted((repo_root / "agent-runs").glob("**/implementer-prompt*.md")))


def _test_functions(source: str, path: Path, repo_root: Path) -> tuple[tuple[int, TestReference], ...]:
    tree = ast.parse(source, filename=str(path))
    test_nodes = (
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
    )
    functions: list[tuple[int, TestReference]] = []
    for node in test_nodes:
        start_line = min([node.lineno, *(decorator.lineno for decorator in node.decorator_list)])
        functions.append(
            (
                start_line,
                TestReference(
                    path=_relative_path(path, repo_root),
                    name=node.name,
                    line=node.lineno,
                ),
            )
        )
    return tuple(sorted(functions))


def collect_test_references(repo_root: Path) -> dict[RequirementId, tuple[TestReference, ...]]:
    """Collect ``# verifies:`` markers and attach them to following tests."""

    references: defaultdict[RequirementId, set[TestReference]] = defaultdict(set)
    tests_dir = repo_root / "tests"
    if not tests_dir.is_dir():
        return {}

    for path in sorted(tests_dir.glob("**/*.py")):
        source = path.read_text(encoding="utf-8")
        test_functions = _test_functions(source, path, repo_root)
        for line_number, line in enumerate(source.splitlines(), start=1):
            following_test = next(
                (reference for start_line, reference in test_functions if start_line > line_number), None
            )
            if following_test is None:
                continue
            for marker_match in MARKER_RE.finditer(line):
                references[_requirement_id(marker_match)].add(following_test)

    return {requirement_id: tuple(sorted(items)) for requirement_id, items in references.items()}


def _section_title(line: str) -> str | None:
    match = SECTION_HEADING_RE.match(line)
    if match is None:
        return None
    return _normalise_title(BRACKET_REQUIREMENT_RE.sub("", match["title"]))


def _direct_title(line: str) -> str | None:
    match = DIRECT_BRACKET_RE.match(line)
    if match is None:
        return None
    value = match["title"]
    if value.startswith("**") and "**" in value[2:]:
        value = value[2:].split("**", maxsplit=1)[0]
    else:
        value = value.split(":", maxsplit=1)[0]
    return _normalise_title(value)


def collect_definitions(
    repo_root: Path,
    known_families: set[str],
) -> dict[RequirementId, Definition]:
    """Discover canonical definitions plus legacy bracket/range definitions.

    New prompts use the explicit bold ``ID — title`` convention.  Older
    Phase-5 prompts used bracketed IDs and ranges, so those are accepted only
    for families independently discovered from test markers or canonical
    definitions.  That retains dynamic family discovery without mistaking
    ordinary ``DEC`` or ``FR`` references for requirements.
    """

    prompt_files = _prompt_files(repo_root)
    definitions: dict[RequirementId, Definition] = {}

    for path in prompt_files:
        source_path = _relative_path(path, repo_root)
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for match in CANONICAL_REQUIREMENT_RE.finditer(line):
                requirement_id = _requirement_id(match)
                known_families.add(requirement_id.family)
                _record_definition(
                    definitions,
                    Definition(
                        requirement_id=requirement_id,
                        title=_normalise_title(match["title"]),
                        source_path=source_path,
                        line=line_number,
                        priority=3,
                    ),
                )

    for path in prompt_files:
        source_path = _relative_path(path, repo_root)
        section_title = "Requirement definition"
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            section_title = _section_title(line) or section_title
            direct_title = _direct_title(line)
            for match in BRACKET_REQUIREMENT_RE.finditer(line):
                if match["family"] not in known_families:
                    continue
                priority = 2 if direct_title is not None else 1
                title = direct_title or section_title
                for requirement_id in _bracket_requirement_ids(match):
                    _record_definition(
                        definitions,
                        Definition(
                            requirement_id=requirement_id,
                            title=title,
                            source_path=source_path,
                            line=line_number,
                            priority=priority,
                        ),
                    )

    return definitions


def _markdown_escape(value: str) -> str:
    return value.replace("|", "\\|")


def _definition_reference(definition: Definition) -> str:
    href = f"../{definition.source_path}#L{definition.line}"
    path = f"{definition.source_path}:{definition.line}"
    return f"[`{path}`]({href})<br>{_markdown_escape(definition.title)}"


def _test_reference(reference: TestReference) -> str:
    href = f"../{reference.path}#L{reference.line}"
    label = f"{reference.path}::{reference.name}"
    return f"[`{label}`]({href})"


def render_traceability(repo_root: Path) -> str:
    """Return the complete deterministic Markdown matrix for ``repo_root``."""

    test_references = collect_test_references(repo_root)
    known_families = {requirement_id.family for requirement_id in test_references}
    definitions = collect_definitions(repo_root, known_families)
    requirement_ids = sorted(set(definitions) | set(test_references))
    families = sorted({requirement_id.family for requirement_id in requirement_ids})

    lines = [
        "<!-- Generated by `uv run python tools/traceability.py`; do not edit manually. -->",
        "",
        "# Requirement Traceability Matrix",
        "",
        "Regenerate this file with `uv run python tools/traceability.py`. The generator scans "
        "`agent-runs/**/implementer-prompt*.md` for requirement definitions and `tests/` for "
        "`# verifies:` markers.",
        "",
        "> Requirement families owned by other repositories are outside this matrix's scope.",
        "",
    ]

    for family in families:
        lines.extend(
            [
                f"## {family}",
                "",
                "| ID | Defining document | Verifying tests | Status |",
                "| --- | --- | --- | --- |",
            ]
        )
        for requirement_id in (item for item in requirement_ids if item.family == family):
            definition = definitions.get(requirement_id)
            tests = test_references.get(requirement_id, ())
            if definition is not None and tests:
                status = "Mapped"
            elif definition is not None:
                status = "Defined but unverified"
            else:
                status = "Verified but undefined"
            defining_document = _definition_reference(definition) if definition is not None else "—"
            verifying_tests = "<br>".join(_test_reference(reference) for reference in tests) if tests else "—"
            lines.append(f"| `{requirement_id.label}` | {defining_document} | {verifying_tests} | {status} |")
        lines.append("")

    defined_but_unverified = [
        requirement_id
        for requirement_id in requirement_ids
        if requirement_id in definitions and requirement_id not in test_references
    ]
    verified_but_undefined = [
        requirement_id
        for requirement_id in requirement_ids
        if requirement_id not in definitions and requirement_id in test_references
    ]

    lines.extend(["## Defined but unverified", ""])
    if defined_but_unverified:
        for requirement_id in defined_but_unverified:
            definition = definitions[requirement_id]
            lines.append(f"- `{requirement_id.label}` — {_definition_reference(definition)}")
    else:
        lines.append("None.")

    lines.extend(["", "## Verified but undefined", ""])
    if verified_but_undefined:
        for requirement_id in verified_but_undefined:
            lines.append(f"- `{requirement_id.label}`")
    else:
        lines.append("None.")

    return "\n".join(lines) + "\n"


def generate_traceability(repo_root: Path, output_path: Path) -> str:
    """Write and return the deterministic matrix."""

    rendered = render_traceability(repo_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    return rendered


def traceability_is_current(repo_root: Path, output_path: Path) -> bool:
    """Return whether the committed matrix matches current prompt/test inputs."""

    return output_path.is_file() and output_path.read_text(encoding="utf-8") == render_traceability(repo_root)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate the repository requirement traceability matrix")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="repository root to scan (default: this tool's repository)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="output Markdown path (default: <repo-root>/docs/TRACEABILITY.md)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when the output differs from a freshly generated matrix",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    output_path = (args.output or repo_root / DEFAULT_OUTPUT_RELATIVE_PATH).resolve()

    if args.check:
        if traceability_is_current(repo_root, output_path):
            print(f"Traceability matrix is current: {output_path}")
            return 0
        print(
            "Traceability matrix is stale; regenerate and commit with `uv run python tools/traceability.py`.",
            file=sys.stderr,
        )
        return 1

    generate_traceability(repo_root, output_path)
    print(f"Wrote traceability matrix: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
