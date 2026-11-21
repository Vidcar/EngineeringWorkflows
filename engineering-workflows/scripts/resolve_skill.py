#!/usr/bin/env python3
"""Resolve exact frontmatter names without relying on directory names."""
import argparse
import json
import os
import re
from pathlib import Path


def skill_name(path):
    if path.is_symlink():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    if not text.startswith("---\n"):
        return None
    head = text.split("---", 2)
    if len(head) < 3:
        return None
    match = re.search(r"^name:\s*['\"]?([a-z0-9]+(?:-[a-z0-9]+)*)['\"]?\s*$", head[1], re.M)
    return match.group(1) if match else None


def resolve(name, roots, include_disabled=False):
    matches = []
    for root in roots:
        root = Path(root).resolve()
        if not root.is_dir():
            continue
        visited = {}
        for current, dirs, files in os.walk(root, followlinks=True):
            depth = len(Path(current).relative_to(root).parts)
            if depth > 8:
                dirs[:] = []
                continue
            try:
                canonical = Path(current).resolve()
            except (OSError, RuntimeError):
                dirs[:] = []
                continue
            # Stop link cycles, but revisit a shallower alias so its descendants
            # are not lost to the traversal depth limit.
            if canonical in visited and visited[canonical] <= depth:
                dirs[:] = []
                continue
            visited[canonical] = depth
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__"}
                       and (include_disabled or d != "uninstalled" or Path(current) != root)]
            if "SKILL.md" in files:
                p = Path(current) / "SKILL.md"
                if skill_name(p) == name:
                    matches.append(canonical)
    matches = sorted(set(matches))
    if len(matches) != 1:
        raise ValueError(f"Expected one active {name}; found {len(matches)}: " + ", ".join(map(str, matches)))
    return matches[0]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name")
    p.add_argument("--root", action="append", required=True)
    p.add_argument("--include-disabled", action="store_true")
    a = p.parse_args()
    try:
        path = resolve(a.name, a.root, a.include_disabled)
        print(json.dumps({"name": a.name, "directory": str(path), "skill_file": str(path / "SKILL.md")}))
    except ValueError as e:
        p.exit(1, str(e) + "\n")


if __name__ == "__main__":
    main()
