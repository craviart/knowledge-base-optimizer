#!/usr/bin/env python3
"""Read-only audit for local knowledge-base organization and context load."""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


MARKDOWN_EXTENSIONS = {".md", ".mdc", ".markdown"}
LOADER_NAMES = {
    "agents.md",
    "agent.md",
    "instructions.md",
    "readme.md",
    "skill.md",
    "claude.md",
    "cursor.mdc",
}
STARTUP_HINTS = (
    "agent-start",
    "quick-context",
    "context",
    "preferences",
    "rules",
    "loader",
)
IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".cache",
}
TOKEN_WORD_RATIO = 0.75
REFERENCE_EXTENSIONS = {
    ".md",
    ".mdc",
    ".markdown",
    ".txt",
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".csv",
    ".tsv",
    ".html",
}
DERIVED_HINTS = (
    "draft",
    "output",
    "export",
    "report",
    "summary",
    "index",
    "archive",
)
SOURCE_HINTS = (
    "source",
    "truth",
    "canonical",
    "glossary",
    "metrics",
    "okr",
    "policy",
    "spec",
    "requirements",
    "guidelines",
    "handbook",
)
STARTUP_WORD_WARNING = 500


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            yield base / filename


def is_markdown(path: Path) -> bool:
    return path.suffix.lower() in MARKDOWN_EXTENSIONS


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def likely_loader(path: Path, root: Path) -> bool:
    name = path.name.lower()
    relative = rel(path, root).lower()
    return (
        name in LOADER_NAMES
        or "/.cursor/rules/" in f"/{relative}"
        or "/.agents/skills/" in f"/{relative}"
        or any(hint in name for hint in STARTUP_HINTS)
    )


def top_level_summary(root: Path) -> list[str]:
    rows = []
    try:
        children = sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        return rows
    for child in children:
        marker = "/" if child.is_dir() else ""
        rows.append(f"- {child.name}{marker}")
    return rows


def find_markdown_links(text: str) -> list[str]:
    links = []
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if (
            not target
            or "://" in target
            or target.startswith("#")
            or target.startswith("mailto:")
            or target.startswith("<")
        ):
            continue
        links.append(target.split("#", 1)[0])
    return links


def link_risks(markdown_files: list[Path], root: Path) -> list[str]:
    risks = []
    for path in markdown_files:
        text = read_text(path)
        for target in find_markdown_links(text):
            if target.startswith("/"):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                risks.append(f"{rel(path, root)} -> {target}")
    return risks


def path_reference_risks(markdown_files: list[Path], root: Path) -> list[str]:
    patterns = [
        re.compile(r"\.\./[A-Z][^\s)]+"),
        re.compile(r"/(?:Users|home|var|tmp|opt)/[^\s)]+"),
        re.compile(r"[A-Za-z]:\\[^\s)]+"),
    ]
    risks = []
    for path in markdown_files:
        text = read_text(path)
        for pattern in patterns:
            for match in pattern.finditer(text):
                risks.append(f"{rel(path, root)}: {match.group(0)}")
                if len(risks) >= 40:
                    return risks
    return risks


def duplicate_filename_rows(files: list[Path], root: Path) -> list[str]:
    by_name: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        if path.name.startswith("."):
            continue
        by_name[path.name.lower()].append(path)

    rows = []
    for name, paths in sorted(by_name.items()):
        if len(paths) < 2:
            continue
        source_like = [path for path in paths if is_reference_like(path)]
        risk = "possible source-of-truth conflict" if len(source_like) > 1 else "duplicate filename"
        joined = "; ".join(rel(path, root) for path in sorted(paths))
        rows.append(f"- {name}: {risk}: {joined}")
    return rows


def is_reference_like(path: Path) -> bool:
    if path.suffix.lower() not in REFERENCE_EXTENSIONS:
        return False
    lower = str(path).lower()
    if any(hint in lower for hint in DERIVED_HINTS):
        return False
    return True


def source_conflict_rows(files: list[Path], root: Path) -> list[str]:
    rows = []
    for path in sorted(files, key=lambda p: rel(p, root).lower()):
        lower = rel(path, root).lower()
        if "index" in path.name.lower() or "/sources/indexes/" in f"/{lower}":
            continue
        if path.suffix.lower() not in REFERENCE_EXTENSIONS:
            continue
        if any(hint in lower for hint in SOURCE_HINTS) and any(
            hint in lower for hint in DERIVED_HINTS
        ):
            rows.append(f"- {rel(path, root)}: source and derived-output hints both present")
    return rows[:40]


def gather_reference_text(markdown_files: list[Path], root: Path) -> str:
    chunks = []
    for path in markdown_files:
        relative = rel(path, root).lower()
        name = path.name.lower()
        if (
            likely_loader(path, root)
            or "index" in name
            or "key-link" in name
            or "recurring-doc" in name
            or "/sources/indexes/" in f"/{relative}"
        ):
            chunks.append(read_text(path).lower())
            chunks.append(relative)
    return "\n".join(chunks)


def unreferenced_rows(files: list[Path], markdown_files: list[Path], root: Path) -> list[str]:
    reference_text = gather_reference_text(markdown_files, root)
    if not reference_text:
        return []

    rows = []
    for path in sorted(files, key=lambda p: rel(p, root).lower()):
        if not is_reference_like(path):
            continue
        relative = rel(path, root)
        lower_relative = relative.lower()
        if "/archive/" in f"/{lower_relative}":
            continue
        if likely_loader(path, root):
            continue

        stem = path.stem.lower()
        tokens = [token for token in re.split(r"[-_\s.]+", stem) if len(token) > 2]
        referenced = lower_relative in reference_text or path.name.lower() in reference_text
        if not referenced and tokens:
            referenced = all(token in reference_text for token in tokens[:4])
        if not referenced:
            rows.append(f"- {relative}")
        if len(rows) >= 40:
            break
    return rows


def archive_readiness_rows(root: Path) -> list[str]:
    rows = []
    archive_dir = root / "archive"
    reports_dir = root / "outputs" / "reports"
    if archive_dir.is_dir():
        rows.append("- archive/: present")
    else:
        rows.append("- archive/: missing")

    if reports_dir.is_dir():
        rows.append("- outputs/reports/: present")
    else:
        rows.append("- outputs/reports/: missing")

    manifest_patterns = ("manifest", "checksum", "sha256", "path-map", "migration")
    candidates = []
    for base in (archive_dir, reports_dir):
        if not base.exists():
            continue
        for path in iter_files(base):
            lower = path.name.lower()
            if any(pattern in lower for pattern in manifest_patterns):
                candidates.append(rel(path, root))
    if candidates:
        rows.append("- migration records found: " + "; ".join(sorted(candidates)[:12]))
    else:
        rows.append("- migration records found: none")
    return rows


def markdown_health_rows(markdown_files: list[Path], root: Path) -> list[str]:
    rows = []
    for path in sorted(markdown_files, key=lambda p: rel(p, root).lower()):
        text = read_text(path)
        stripped = text.strip()
        relative = rel(path, root)
        issues = []
        if not stripped:
            issues.append("empty file")
        elif not re.search(r"^#\s+", text, re.MULTILINE):
            issues.append("missing top-level heading")
        if re.search(r"\b(TODO|FIXME|TBD)\b", text, re.IGNORECASE):
            issues.append("contains TODO/FIXME/TBD")
        if issues:
            rows.append(f"- {relative}: {', '.join(issues)}")
        if len(rows) >= 40:
            break
    return rows


def maintenance_readiness_rows(
    root: Path, markdown_files: list[Path], loader_words: int
) -> list[str]:
    rows = []
    agent_start = root / "identity" / "agent-start.md"
    if agent_start.exists():
        rows.append("- compact startup file: present")
    else:
        rows.append("- compact startup file: missing")

    if loader_words > STARTUP_WORD_WARNING:
        rows.append(
            f"- likely loader words: {loader_words}, above {STARTUP_WORD_WARNING}-word target"
        )
    else:
        rows.append(
            f"- likely loader words: {loader_words}, within {STARTUP_WORD_WARNING}-word target"
        )

    index_files = [
        path
        for path in markdown_files
        if "index" in path.name.lower() or "/sources/indexes/" in f"/{rel(path, root).lower()}"
    ]
    rows.append(f"- index-like Markdown files: {len(index_files)}")

    source_like_count = sum(1 for path in iter_files(root) if is_reference_like(path))
    rows.append(f"- reference-like files to keep routed: {source_like_count}")
    return rows


def print_rows(title: str, rows: list[str], empty: str = "None found.") -> None:
    print(f"\n## {title}")
    if rows:
        for row in rows:
            print(row)
    else:
        print(empty)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only audit for knowledge-base structure and context-load cost."
    )
    parser.add_argument("root", help="Path to the knowledge-base root")
    parser.add_argument(
        "--top",
        type=int,
        default=12,
        help="Number of largest Markdown files to show",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        parser.error(f"root must be an existing directory: {root}")

    files = list(iter_files(root))
    markdown_files = [path for path in files if is_markdown(path)]
    counts = [(path, word_count(read_text(path))) for path in markdown_files]
    counts.sort(key=lambda item: item[1], reverse=True)

    loader_counts = [(path, count) for path, count in counts if likely_loader(path, root)]
    loader_words = sum(count for _, count in loader_counts)
    total_words = sum(count for _, count in counts)
    suffix_counts = Counter(path.suffix.lower() or "[no extension]" for path in files)

    expected_dirs = ["identity", "playbooks", "sources", "outputs", "reviews", "archive"]
    missing_expected_dirs = [name for name in expected_dirs if not (root / name).is_dir()]

    print("# Knowledge Base Audit")
    print(f"Root: {root}")
    print(f"Files scanned: {len(files)}")
    print(f"Markdown-like files: {len(markdown_files)}")
    print(f"Markdown words: {total_words}")
    print(f"Estimated Markdown tokens: {round(total_words / TOKEN_WORD_RATIO)}")
    print(f"Likely loader words: {loader_words}")
    print(f"Estimated loader tokens: {round(loader_words / TOKEN_WORD_RATIO)}")

    print_rows("Top-Level Tree", top_level_summary(root))

    print("\n## File Types")
    for suffix, count in suffix_counts.most_common(12):
        print(f"- {suffix}: {count}")

    largest_rows = [
        f"- {rel(path, root)}: {count} words, about {round(count / TOKEN_WORD_RATIO)} tokens"
        for path, count in counts[: args.top]
    ]
    print_rows("Largest Markdown Files", largest_rows)

    loader_rows = [
        f"- {rel(path, root)}: {count} words, about {round(count / TOKEN_WORD_RATIO)} tokens"
        for path, count in sorted(loader_counts, key=lambda item: rel(item[0], root).lower())
    ]
    print_rows("Likely Startup Or Routing Files", loader_rows)

    structure_rows = [
        f"- Missing recommended folder: {name}/" for name in missing_expected_dirs
    ]
    if not (root / "identity" / "agent-start.md").exists():
        structure_rows.append("- Missing compact startup candidate: identity/agent-start.md")
    if not (root / "sources" / "indexes").is_dir():
        structure_rows.append("- Missing lightweight index folder: sources/indexes/")
    if not (root / "sources" / "sources").is_dir():
        structure_rows.append("- Missing canonical source shelf candidate: sources/sources/")
    print_rows("Structure Opportunities", structure_rows)

    print_rows("Archive Readiness", archive_readiness_rows(root))
    print_rows("Maintenance Readiness", maintenance_readiness_rows(root, markdown_files, loader_words))
    print_rows("Markdown Health Risks", markdown_health_rows(markdown_files, root))
    print_rows("Duplicate Filename Risks", duplicate_filename_rows(files, root))
    print_rows("Possible Source Conflicts", source_conflict_rows(files, root))
    print_rows("Unreferenced Reference-Like Files", unreferenced_rows(files, markdown_files, root))
    print_rows("Broken Relative Markdown Link Risks", link_risks(markdown_files, root)[:40])
    print_rows("Path Reference Risks", path_reference_risks(markdown_files, root))

    print("\n## Optimization Prompt")
    print(
        "Preserve original files, manifests, checksums, and path maps before changing structure. "
        "Then compare the likely loader word count with a compact startup target under 500 words, "
        "and route task-specific work to indexes or canonical sources only when needed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
