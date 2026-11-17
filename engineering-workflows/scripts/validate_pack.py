#!/usr/bin/env python3
"""Validate installed engineering pack files and declarations, not agent behavior."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    raise SystemExit("Pack validation needs PyYAML in the current Python environment.")

from resolve_skill import resolve


ACTIVE_NAMES = {
    "engineering-workflows", "engineering-check", "engineering-verify",
    "engineering-measure", "engineering-arena", "engineering-campaign",
    "engineering-configure",
}
ADMIN_NAMES = {"engineering-campaign", "engineering-configure"}
NAME_PATTERN = r"engineering-[a-z0-9]+(?:-[a-z0-9]+)*"


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently taking the last value."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(text):
    return yaml.load(text, Loader=UniqueKeyLoader)


def frontmatter(path):
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    data = read_yaml(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter must be an object: {path}")
    return data, content[match.end():]


def file_within(directory, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        return False
    target = (directory / relative).resolve()
    return target.is_relative_to(directory) and target.is_file()


def string_list(value, label):
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{label} must be a list of nonempty strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} contains duplicates")
    return value


def read_manifest(path):
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 3:
        raise ValueError("Unsupported manifest schema: expected schema_version 3")
    if not isinstance(manifest.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise ValueError("Manifest version must be a semantic version such as 2.0.0")
    nodes = manifest.get("skills")
    if not isinstance(nodes, list) or any(not isinstance(node, dict) for node in nodes):
        raise ValueError("Manifest skills must be a list of objects")
    names = [node.get("name") for node in nodes]
    if any(not isinstance(name, str) or not re.fullmatch(NAME_PATTERN, name) for name in names):
        raise ValueError("Manifest contains an invalid skill name")
    if len(names) != len(set(names)):
        raise ValueError("Manifest has duplicate names")
    if type(manifest.get("expected_skill_count")) is not int or manifest["expected_skill_count"] != 7 or len(names) != 7:
        raise ValueError("Manifest expected_skill_count and declared skill count must both be 7")
    if set(names) != ACTIVE_NAMES:
        raise ValueError("Manifest must declare exactly the seven active engineering skills")
    for node in nodes:
        name = node["name"]
        if not isinstance(node.get("role"), str) or not node["role"].strip():
            raise ValueError(f"{name}: role must be a nonempty string")
        if type(node.get("disable_model_invocation")) is not bool:
            raise ValueError(f"{name}: invocation policy must be a Boolean")
        if type(node.get("user_request_required")) is not bool:
            raise ValueError(f"{name}: user_request_required must be a Boolean")
        string_list(node.get("auto_calls"), f"{name}: auto_calls")
        string_list(node.get("required_files"), f"{name}: required_files")
    string_list(manifest.get("shared_references"), "shared_references")
    return manifest


def markdown_targets(content):
    # Inline links/images and reference definitions; anchors need no file check.
    inline = re.findall(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", content)
    definitions = re.findall(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", content, re.M)
    return inline + definitions


def validate(roots, manifest_path=None):
    roots = list(roots)
    errors, paths = [], {}
    try:
        core = resolve("engineering-workflows", roots)
        manifest = read_manifest(Path(manifest_path) if manifest_path else core / "references/pack-contract.json")
    except (ValueError, OSError, TypeError) as error:
        return {"valid": False, "errors": [str(error)]}

    nodes = manifest["skills"]
    by_name = {node["name"]: node for node in nodes}
    for node in nodes:
        name = node["name"]
        if node["user_request_required"] != (name in ADMIN_NAMES):
            errors.append(f"{name}: user_request_required must be true only for Campaign and Configure")
        if name in ADMIN_NAMES and node["disable_model_invocation"]:
            errors.append(f"{name}: administrative skill must permit natural-language selection")
        try:
            directory = resolve(name, roots)
            paths[name] = directory
            data, _ = frontmatter(directory / "SKILL.md")
            if set(data) != {"name", "description"}:
                errors.append(f"{name}: expected only name and description frontmatter")
            if data.get("name") != name:
                errors.append(f"{name}: frontmatter name mismatch")
            description = data.get("description")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                errors.append(f"{name}: description must be a nonempty string of at most 1024 characters")
            elif "<" in description or ">" in description:
                errors.append(f"{name}: angle brackets in description")
            ui = read_yaml((directory / "agents/openai.yaml").read_text(encoding="utf-8"))
            if not isinstance(ui, dict) or not isinstance(ui.get("policy"), dict) or not isinstance(ui.get("interface"), dict):
                raise ValueError("agents/openai.yaml must contain interface and policy objects")
            if ui["policy"].get("allow_implicit_invocation") is not (not node["disable_model_invocation"]):
                errors.append(f"{name}: native invocation policy mismatch")
            interface = ui["interface"]
            prompt = interface.get("default_prompt")
            if not isinstance(prompt, str) or not re.search(r"\$" + re.escape(name) + r"(?![a-z0-9-])", prompt):
                errors.append(f"{name}: UI prompt does not name its actual skill")
            short = interface.get("short_description")
            if not isinstance(short, str) or not 25 <= len(short) <= 64:
                errors.append(f"{name}: UI short description must be 25–64 characters")
            if not isinstance(interface.get("display_name"), str) or not interface["display_name"].strip():
                errors.append(f"{name}: UI display_name must be nonempty")
            for key in ("icon_small", "icon_large"):
                if key in interface and not file_within(directory, interface[key]):
                    errors.append(f"{name}: missing/unsafe {key}: {interface[key]}")
            for relative in node["required_files"]:
                if not file_within(directory, relative):
                    errors.append(f"{name}: required file missing/unsafe: {relative}")
            # Core files are checked even if omitted from the required_files list.
            if not (directory / "LICENSE").is_file():
                errors.append(f"{name}: missing LICENSE")
            for file in directory.rglob("*.md"):
                content = file.read_text(encoding="utf-8")
                for target in markdown_targets(content):
                    parts = urlsplit(target.strip("<>"))
                    if parts.scheme or not parts.path:
                        continue
                    relative = unquote(parts.path)
                    local = (file.parent / relative).resolve()
                    if Path(relative).is_absolute() or not local.is_relative_to(directory) or not local.exists():
                        errors.append(f"{name}: broken/escaping link {target} in {file.relative_to(directory)}")
        except (ValueError, OSError, TypeError, yaml.YAMLError) as error:
            errors.append(f"{name}: {error}")

    graph = {node["name"]: node["auto_calls"] for node in nodes}
    for name, calls in graph.items():
        for target in calls:
            if target not in by_name:
                errors.append(f"{name}: unknown automatic callee {target}")
            else:
                if by_name[target]["disable_model_invocation"]:
                    errors.append(f"{name}: automatic edge to explicit-only {target}")
                if by_name[target]["user_request_required"]:
                    errors.append(f"{name}: automatic edge to user-request-only {target}")
    visited, active = set(), []

    def visit(name):
        if name in active:
            errors.append("Automatic call cycle: " + " -> ".join(active + [name]))
            return
        if name in visited:
            return
        active.append(name)
        for target in graph.get(name, []):
            visit(target)
        active.pop()
        visited.add(name)

    for name in graph:
        visit(name)
    for relative in manifest["shared_references"]:
        if not file_within(core, relative):
            errors.append(f"Missing/unsafe shared reference: {relative}")
    return {
        "valid": not errors, "schema_version": manifest["schema_version"], "version": manifest["version"],
        "skill_count": len(paths), "explicit_only": [node["name"] for node in nodes if node["disable_model_invocation"]],
        "user_request_only": [node["name"] for node in nodes if node["user_request_required"]],
        "automatic_edges": sum(map(len, graph.values())), "errors": errors,
        "limit": "Checks installed files, schemas, declared policies and graph; semantic consistency and host registration require separate verification.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", required=True, help="Canonical installed skill root (repeatable)")
    parser.add_argument("--manifest", help="Optional alternate contract for diagnosis")
    args = parser.parse_args()
    result = validate(args.root, args.manifest)
    print(json.dumps(result, indent=2))
    raise SystemExit(not result["valid"])


if __name__ == "__main__":
    main()
