#!/usr/bin/env python3
"""Validate every SKILL.md frontmatter in the repo.

Checks:
  - frontmatter block exists and is valid YAML
  - `name` exists, matches `category:skill-name` pattern
  - `name` matches the path: <category>/<skill-name>/SKILL.md
  - `description` exists and is non-empty
  - `argument-hint`, if present, is a string or a single-element list
    (a value like `[a] [b]` parses as a 1-element list with junk and
    silently breaks downstream tools — reject it)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
NAME_RE = re.compile(r"^[a-z][a-z0-9-]*:[a-z][a-z0-9-]*$")
FRONT_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def validate(skill_path: Path) -> list[str]:
    errors: list[str] = []
    rel = skill_path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) != 3 or parts[-1] != "SKILL.md":
        return [f"{rel}: SKILL.md must live at <category>/<skill-name>/SKILL.md"]

    expected_name = f"{parts[0]}:{parts[1]}"
    text = skill_path.read_text(encoding="utf-8")

    m = FRONT_RE.match(text)
    if not m:
        return [f"{rel}: missing or malformed frontmatter block"]

    raw = m.group(1)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return [f"{rel}: invalid YAML frontmatter — {e}"]

    if not isinstance(data, dict):
        return [f"{rel}: frontmatter must be a YAML mapping"]

    name = data.get("name")
    if not name:
        errors.append(f"{rel}: missing 'name'")
    elif not isinstance(name, str) or not NAME_RE.match(name):
        errors.append(
            f"{rel}: name {name!r} must match pattern 'category:skill-name' (kebab-case)"
        )
    elif name != expected_name:
        errors.append(
            f"{rel}: name {name!r} must match path → expected {expected_name!r}"
        )

    desc = data.get("description")
    if not desc or not str(desc).strip():
        errors.append(f"{rel}: missing or empty 'description'")

    hint = data.get("argument-hint")
    if hint is not None and not isinstance(hint, (str, list)):
        errors.append(
            f"{rel}: 'argument-hint' must be a string or list, got {type(hint).__name__} — "
            f"a value like '[a] [b]' parses as a 1-element list and breaks tooling; quote it"
        )

    return errors


def main() -> int:
    skill_files = sorted(ROOT.glob("*/*/SKILL.md"))
    all_errors: list[str] = []
    for skill in skill_files:
        all_errors.extend(validate(skill))

    if all_errors:
        print("Skill validation failed:\n", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) across {len(skill_files)} skill(s).", file=sys.stderr)
        return 1

    print(f"All {len(skill_files)} skills passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
