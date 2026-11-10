#!/usr/bin/env python3
"""Check this repository without installing packages or running skill scaffolds.

The skill archives contain illustrative code blocks. This script does not
execute them. It checks text encoding, JSON, SKILL.md frontmatter, local
Markdown references, and byte-for-byte preservation of the imported skill files.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "scripts" / "source-manifest.json"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
PATH_RE = re.compile(r"`([^`\n]+)`")
JSON_FENCE_RE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)

SKIP_DIR_NAMES = {".git", "__pycache__", "__MACOSX"}
JUNK_NAMES = {".DS_Store"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.counts: dict[str, int] = {}

    def error(self, message: str) -> None:
        self.errors.append(message)

    def add(self, key: str, n: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + n


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def is_junk(path: Path) -> bool:
    return (
        path.name in JUNK_NAMES
        or path.name.startswith("._")
        or "__MACOSX" in path.parts
    )


def read_utf8(path: Path, report: Report) -> str | None:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        report.error(f"UTF-8 BOM is not used in this repo: {path.relative_to(ROOT)}")
        return None
    if b"\x00" in data:
        report.error(f"NUL byte in {path.relative_to(ROOT)}")
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        report.error(f"not UTF-8: {path.relative_to(ROOT)}: {exc}")
        return None


def github_slug(title: str) -> str:
    text = title.strip().lower()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    kept: list[str] = []
    for char in text:
        category = unicodedata.category(char)
        if char.isalnum() or char in " -" or category.startswith(("L", "N")):
            kept.append(char)
    slug = re.sub(r"\s+", "-", "".join(kept))
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def heading_slugs(markdown: str) -> set[str]:
    body = FENCE_RE.sub("", markdown)
    slugs: set[str] = set()
    seen: dict[str, int] = {}
    for match in HEADING_RE.finditer(body):
        base = github_slug(match.group(2))
        if not base:
            continue
        count = seen.get(base, 0)
        seen[base] = count + 1
        slugs.add(base if count == 0 else f"{base}-{count}")
    return slugs


def parse_frontmatter(text: str, rel: Path, report: Report) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        report.error(f"{rel}: SKILL.md does not start with frontmatter")
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        report.error(f"{rel}: unterminated frontmatter")
        return None
    fields: dict[str, str] = {}
    for line_no, line in enumerate(text[4:end].splitlines(), start=2):
        if not line.strip():
            continue
        if ":" not in line:
            report.error(f"{rel}:{line_no}: frontmatter line is not key: value")
            continue
        key, value = line.split(":", 1)
        if key in fields:
            report.error(f"{rel}:{line_no}: duplicate frontmatter key {key}")
        fields[key] = value.strip()
    for required in ("name", "description"):
        if required not in fields or not fields[required]:
            report.error(f"{rel}: missing frontmatter {required}")
    name = fields.get("name", "")
    if name and not NAME_RE.fullmatch(name):
        report.error(f"{rel}: name {name!r} is not a lowercase skill name")
    if name and rel.parent.name != name:
        report.error(
            f"{rel}: name {name!r} does not match parent directory {rel.parent.name!r}"
        )
    description = fields.get("description", "")
    if description and not 1 <= len(description) <= 1024:
        report.error(
            f"{rel}: description length {len(description)} is outside 1..1024"
        )
    report.add("skill_frontmatter")
    return fields


def check_markdown(path: Path, text: str, texts: dict[Path, str], report: Report) -> None:
    rel = path.relative_to(ROOT)
    if path.name == "SKILL.md":
        parse_frontmatter(text, rel, report)
    slugs_by_file = {item: heading_slugs(body) for item, body in texts.items()}
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:")):
            report.add("external_links")
            continue
        path_part, sep, anchor = target.partition("#")
        path_part = path_part.strip()
        if not path_part and not sep:
            report.error(f"{rel}: empty link target")
            continue
        report.add("local_links")
        if path_part:
            destination = (path.parent / path_part).resolve()
            try:
                destination.relative_to(ROOT)
            except ValueError:
                report.error(f"{rel}: link escapes the repo: {target}")
                continue
            if not destination.is_file():
                report.error(f"{rel}: missing link target {target}")
                continue
        else:
            destination = path
        if sep:
            anchor = anchor.strip()
            if anchor.startswith("L") and anchor[1:].isdigit() and destination.suffix != ".md":
                continue
            if destination.suffix == ".md" and anchor not in slugs_by_file.get(destination, set()):
                report.error(f"{rel}: missing heading #{anchor} in {destination.relative_to(ROOT)}")
    if path.suffix == ".md":
        for match in JSON_FENCE_RE.finditer(text):
            report.add("json_fences")
            try:
                json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                report.error(f"{rel}: JSON fence does not parse: {exc}")
        for match in PATH_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith(("http://", "https://")):
                continue
            if not (
                raw.startswith(("references/", "assets/", "skills/", "examples/", "scripts/"))
                or raw.startswith(("./", "../"))
            ):
                continue
            if not raw.endswith((".md", ".json", ".py")):
                continue
            if any(char in raw for char in " \n*?<>|"):
                continue
            report.add("path_mentions")
            destination = (path.parent / raw).resolve()
            if not destination.exists():
                report.error(f"{rel}: missing path mention `{raw}`")


def check_methodology_markers(texts: dict[Path, str], report: Report) -> None:
    english = texts.get(ROOT / "skills/agent-system-design/SKILL.md", "")
    chinese = texts.get(ROOT / "skills/agent-system-design-cn/SKILL.md", "")
    for label, text, needles in (
        (
            "English SKILL.md",
            english,
            (
                "Prompt, Workflow, Single Agent, or Multi-Agent",
                "1 Requirements Clarification",
                "7 Delivery and Self-Review",
                "21 review dimensions",
                "21 Agentic design patterns",
            ),
        ),
        (
            "Chinese SKILL.md",
            chinese,
            (
                "提示词、工作流、单 Agent、多 Agent",
                "1 需求澄清",
                "7 交付与自检",
                "21 个维度",
                "21 种 Agentic 设计模式",
            ),
        ),
    ):
        if not text:
            report.error(f"missing {label}")
            continue
        for needle in needles:
            if needle not in text:
                report.error(f"{label} is missing {needle!r}")

    en_patterns = ROOT / "skills/agent-system-design/references/10-design-pattern-index.md"
    cn_patterns = ROOT / "skills/agent-system-design-cn/references/10-设计模式索引.md"
    en_review = ROOT / "skills/agent-system-design/assets/design-self-review-checklist.md"
    cn_review = ROOT / "skills/agent-system-design-cn/assets/设计自检清单.md"
    expect_rows = {str(number) for number in range(1, 22)}

    def table_ids(text: str) -> set[str]:
        return set(re.findall(r"^\| ([0-9]+) \|", text, re.MULTILINE))

    def heading_ids(text: str, pattern: str) -> set[str]:
        return set(re.findall(pattern, text, re.MULTILINE))

    checks = (
        (en_patterns, table_ids, None, "English pattern rows"),
        (cn_patterns, table_ids, None, "Chinese pattern rows"),
        (en_review, None, r"^### Dimension ([0-9]+):", "English review dimensions"),
        (cn_review, None, r"^### 维度 ([0-9]+)：", "Chinese review dimensions"),
    )
    for path, table_fn, heading_pattern, label in checks:
        text = texts.get(path, "")
        found = table_fn(text) if table_fn else heading_ids(text, heading_pattern or "")
        if found != expect_rows:
            missing = sorted(expect_rows - found, key=int)
            extra = sorted(found - expect_rows, key=int)
            report.error(f"{label}: expected 1..21, missing {missing}, extra {extra}")
        else:
            report.add("methodology_markers")

    for path in (
        ROOT / "skills/agent-system-design/assets/handoff-contract-template.json",
        ROOT / "skills/agent-system-design-cn/assets/交接契约模板.json",
    ):
        text = texts.get(path, "")
        try:
            document = json.loads(text)
        except json.JSONDecodeError as exc:
            report.error(f"{path.relative_to(ROOT)}: {exc}")
            continue
        defs = document.get("$defs", {})
        for key in ("dispatch", "handoff", "gate"):
            if key not in defs:
                report.error(f"{path.relative_to(ROOT)}: missing $defs.{key}")
        required = defs.get("dispatch", {}).get("required", [])
        expected = [
            "identity",
            "objective",
            "scope",
            "constraints",
            "context",
            "output_format",
            "stop_condition",
        ]
        if required != expected:
            report.error(
                f"{path.relative_to(ROOT)}: dispatch required fields are {required!r}"
            )
        report.add("handoff_contracts")


def check_manifest(file_bytes: dict[Path, bytes], report: Report) -> None:
    if not MANIFEST_PATH.is_file():
        report.error("missing scripts/source-manifest.json")
        return
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = manifest.get("imported_skill_files")
    if not isinstance(entries, list):
        report.error("source manifest is missing imported_skill_files")
        return
    seen: set[Path] = set()
    for entry in entries:
        rel = Path(entry["path"])
        path = ROOT / rel
        seen.add(path)
        data = file_bytes.get(path)
        if data is None:
            report.error(f"manifest path missing: {rel}")
            continue
        digest = hashlib.sha256(data).hexdigest()
        if digest != entry["sha256"] or len(data) != entry["bytes"]:
            report.error(f"skill bytes differ from the imported archive: {rel}")
        else:
            report.add("preserved_files")
            report.add("preserved_bytes", len(data))
    skill_files = [
        path
        for path in file_bytes
        if path.relative_to(ROOT).parts[0] == "skills"
    ]
    extra = sorted(set(skill_files) - seen)
    for path in extra:
        report.error(f"unexpected file under skills/: {path.relative_to(ROOT)}")
    if len(entries) != 28:
        report.error(f"expected 28 imported skill files, manifest has {len(entries)}")


def main() -> int:
    report = Report()
    files = iter_files()
    texts: dict[Path, str] = {}
    file_bytes: dict[Path, bytes] = {}
    for path in files:
        rel = path.relative_to(ROOT)
        if is_junk(path):
            report.error(f"junk path should not be committed: {rel}")
            continue
        report.add("files")
        data = path.read_bytes()
        file_bytes[path] = data
        text = read_utf8(path, report)
        if text is None:
            continue
        report.add("utf8_files")
        texts[path] = text
        if path.suffix == ".json":
            try:
                json.loads(text)
                report.add("json_files")
            except json.JSONDecodeError as exc:
                report.error(f"{rel}: JSON does not parse: {exc}")
    for path, text in texts.items():
        if path.suffix == ".md":
            check_markdown(path, text, texts, report)
    check_methodology_markers(texts, report)
    check_manifest(file_bytes, report)

    print("validate_repo")
    for key in sorted(report.counts):
        print(f"  {key}: {report.counts[key]}")
    if report.errors:
        print(f"FAILED {len(report.errors)}")
        for message in report.errors:
            print(f"  - {message}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
