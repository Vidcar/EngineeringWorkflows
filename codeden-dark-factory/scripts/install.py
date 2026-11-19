#!/usr/bin/env python3
"""Install the project-local CodeDen skill pack; preview unless --apply is supplied.

Python 3.10+ and its standard library are sufficient. The installer never changes global
provider settings, .codeden, Git state, or CodeDen itself. Run while the project's
instruction and skill files are not being edited by another process.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from dataclasses import dataclass, field


PACKAGE = "codeden-engineering-skills"
MANIFEST = ".codeden-engineering-skills.json"
LOCK = ".codeden-engineering-skills.install.lock"
BEGIN = "<!-- codeden-engineering-skills:begin -->"
END = "<!-- codeden-engineering-skills:end -->"
PROVIDERS = {
    "codex": (".agents/skills", "AGENTS.md"),
    "claude": (".claude/skills", "CLAUDE.md"),
}


class InstallError(Exception):
    """A collision or invalid input that must be resolved deliberately."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relative_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise InstallError(f"Unsafe relative path: {value!r}")
    path = PurePosixPath(value)
    parts = value.split("/")
    if path.is_absolute() or any(p in ("", ".", "..") for p in parts):
        raise InstallError(f"Unsafe relative path: {value!r}")
    for part in parts:
        if any(ord(c) < 32 for c in part) or ":" in part or part.endswith((" ", ".")):
            raise InstallError(f"Nonportable relative path: {value!r}")
        if part.split(".")[0].upper() in {
            "CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)],
            *[f"LPT{i}" for i in range(1, 10)],
        }:
            raise InstallError(f"Nonportable relative path: {value!r}")
    return value


@dataclass(frozen=True)
class State:
    kind: str
    data: bytes = b""
    mode: int = 0


def state(path: Path) -> State:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return State("missing")
    if stat.S_ISLNK(info.st_mode):
        raise InstallError(f"Symlinks are not allowed: {path}")
    mode = stat.S_IMODE(info.st_mode)
    if stat.S_ISDIR(info.st_mode):
        return State("directory", mode=mode)
    if not stat.S_ISREG(info.st_mode):
        raise InstallError(f"Expected an ordinary file or directory: {path}")
    return State("file", path.read_bytes(), mode)


def project_root(project: Path) -> Path:
    project = Path(os.path.abspath(project))
    # Do not silently follow a symlink supplied as the project or one of its parents.
    for parent in reversed((project, *project.parents)):
        if parent.is_symlink():
            raise InstallError(f"Project path traverses a symlink: {parent}")
    if state(project).kind != "directory":
        raise InstallError(f"Project must be an existing directory: {project}")
    return project


@dataclass
class Write:
    path: str
    data: bytes
    mode: int


@dataclass
class Plan:
    project: Path
    expected: dict[str, State] = field(default_factory=dict)
    writes: list[Write] = field(default_factory=list)

    def inspect(self, relative: str, *, directory: bool = False) -> State:
        parts = relative_path(relative).split("/")
        for index in range(1, len(parts) + 1):
            key = "/".join(parts[:index])
            current = state(self.project / key)
            required = "directory" if index < len(parts) or directory else "file"
            if current.kind not in (required, "missing"):
                raise InstallError(f"Expected {required}, found {current.kind}: {key}")
            previous = self.expected.setdefault(key, current)
            if previous != current:
                raise InstallError(f"File changed while planning: {key}; rerun the preview")
        return current

    def write(self, relative: str, data: bytes, mode: int = 0o644) -> None:
        before = self.inspect(relative)
        if before.kind == "file" and before.data == data:
            return
        self.writes.append(Write(relative, data, before.mode if before.kind == "file" else mode))


def load_manifest(plan: Plan) -> dict:
    before = plan.inspect(MANIFEST)
    if before.kind == "missing":
        return {"schema": 1, "package": PACKAGE, "providers": {}}
    try:
        result = json.loads(before.data)
    except (ValueError, UnicodeDecodeError) as error:
        raise InstallError(f"Cannot parse {MANIFEST}: {error}") from error
    if not isinstance(result, dict) or set(result) != {"schema", "package", "providers"}:
        raise InstallError(f"Unrecognized {MANIFEST}; will not replace it")
    if result["schema"] != 1 or result["package"] != PACKAGE or not isinstance(result["providers"], dict):
        raise InstallError(f"Unrecognized {MANIFEST}; will not replace it")
    for provider, entry in result["providers"].items():
        if provider not in PROVIDERS or not isinstance(entry, dict) or set(entry) != {"files", "instruction"}:
            raise InstallError(f"Invalid provider entry in {MANIFEST}")
        root, instruction = PROVIDERS[provider]
        if not isinstance(entry["files"], dict) or not isinstance(entry["instruction"], dict):
            raise InstallError(f"Invalid ownership entry in {MANIFEST}")
        expected_instruction = entry["instruction"]
        if set(expected_instruction) != {"path", "block_sha256"} or expected_instruction["path"] != instruction:
            raise InstallError(f"Invalid instruction ownership in {MANIFEST}")
        hashes = [expected_instruction["block_sha256"]]
        for path, file_hash in entry["files"].items():
            relative_path(path)
            if not path.startswith(root + "/") or len(PurePosixPath(path).parts) < 4:
                raise InstallError(f"Out-of-scope ownership in {MANIFEST}: {path}")
            hashes.append(file_hash)
        if any(not isinstance(h, str) or re.fullmatch(r"[0-9a-f]{64}", h) is None for h in hashes):
            raise InstallError(f"Invalid content hash in {MANIFEST}")
    return result


def source_files(source: Path) -> dict[str, tuple[bytes, int]]:
    source = project_root(source)
    if state(source).kind != "directory" or state(source / "skills").kind != "directory":
        raise InstallError("The pack must contain a real skills/ directory")
    result: dict[str, tuple[bytes, int]] = {}
    folded: set[str] = set()

    def walk(folder: Path) -> None:
        for path in sorted(folder.iterdir()):
            relative = relative_path(path.relative_to(source / "skills").as_posix())
            current = state(path)
            if relative.casefold() in folded:
                raise InstallError(f"Case-insensitive source path collision: {relative}")
            folded.add(relative.casefold())
            if current.kind == "directory":
                walk(path)
            else:
                result[relative] = (current.data, 0o644 | (current.mode & 0o111))

    names = sorted((source / "skills").iterdir())
    if not names:
        raise InstallError("No skills found in this pack")
    for folder in names:
        if state(folder).kind != "directory" or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", folder.name):
            raise InstallError(f"Expected a real skill directory with a portable name: {folder}")
        for required in ("SKILL.md", "LICENSE"):
            if state(folder / required).kind != "file":
                raise InstallError(f"Skill is missing {required}: {folder.name}")
        walk(folder)
    return result


def block_span(text: str) -> tuple[int, int] | None:
    if BEGIN not in text and END not in text:
        return None
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise InstallError("Malformed routing markers: exactly one begin/end pair is required")
    start, end = text.index(BEGIN), text.index(END)
    if start >= end:
        raise InstallError("Malformed routing markers: end precedes begin")
    for position, marker in ((start, BEGIN), (end, END)):
        after = text[position + len(marker):]
        if (position and text[position - 1] != "\n") or (after and not after.startswith(("\n", "\r\n"))):
            raise InstallError("Routing markers must occupy their own lines")
    return start, end + len(END)


def template_body(source: Path, instruction: str) -> str:
    template = source / "templates" / f"{instruction.removesuffix('.md')}.block.md"
    if state(source / "templates").kind != "directory" or state(template).kind != "file":
        raise InstallError(f"Missing routing template: {template.name}")
    try:
        body = template.read_bytes().decode("utf-8").replace("\r\n", "\n").strip("\n")
    except UnicodeDecodeError as error:
        raise InstallError(f"Routing template is not UTF-8: {template.name}") from error
    if not body.strip() or BEGIN in body or END in body:
        raise InstallError(f"Routing template must be a nonempty body without managed markers: {template.name}")
    return body


def plan_instruction(plan: Plan, source: Path, instruction: str, owned: dict | None) -> str:
    before = plan.inspect(instruction)
    try:
        text = before.data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InstallError(f"{instruction} is not UTF-8; merge the routing manually") from error
    span = block_span(text)
    if owned:
        if not span or digest(text[span[0]:span[1]].encode()) != owned["block_sha256"]:
            raise InstallError(f"Owned routing block was edited or removed: {instruction}; preserve and reconcile it first")
    elif span:
        raise InstallError(f"Unowned routing block exists in {instruction}; will not adopt or replace it")
    eol = "\r\n" if "\r\n" in text else "\n"
    block = eol.join((BEGIN, template_body(source, instruction).replace("\n", eol), END))
    if span:
        updated = text[:span[0]] + block + text[span[1]:]
    else:
        separator = "" if not text or text.endswith(eol * 2) else eol if text.endswith(eol) else eol * 2
        updated = text + separator + block + eol
    plan.write(instruction, updated.encode("utf-8"))
    return digest(block.encode("utf-8"))


def make_plan(source: Path, project: Path, providers: tuple[str, ...]) -> Plan:
    if not providers or len(set(providers)) != len(providers) or any(p not in PROVIDERS for p in providers):
        raise InstallError("Choose codex, claude, or both")
    source = Path(os.path.abspath(source))
    plan = Plan(project_root(project))
    if plan.project == source or source in plan.project.parents or plan.project in source.parents:
        raise InstallError("Choose a target project separate from the distribution pack")
    if state(plan.project / LOCK).kind != "missing":
        raise InstallError(f"An installation lock exists: {LOCK}; resolve the active or interrupted install first")
    if "codex" in providers and state(plan.project / "AGENTS.override.md").kind != "missing":
        raise InstallError("AGENTS.override.md shadows AGENTS.md; reconcile the active Codex instructions before installing")
    manifest = load_manifest(plan)
    files = source_files(source)
    for provider in providers:
        root, instruction = PROVIDERS[provider]
        old = manifest["providers"].get(provider)
        old_files = old["files"] if old else {}
        desired = {f"{root}/{path}": value for path, value in files.items()}
        stale = sorted(set(old_files) - set(desired))
        if stale:
            raise InstallError("Source removed previously installed files; review removal before upgrading: " + ", ".join(stale))
        for path, expected_hash in old_files.items():
            current = plan.inspect(path)
            if current.kind != "file" or digest(current.data) != expected_hash:
                raise InstallError(f"Owned file was edited or removed: {path}; preserve and reconcile it first")
        for name in sorted({path.split("/")[0] for path in files}):
            folder = f"{root}/{name}"
            current = plan.inspect(folder, directory=True)
            if current.kind != "missing" and not any(p.startswith(folder + "/") for p in old_files):
                raise InstallError(f"Unowned skill folder already exists: {folder}; choose an explicit migration")
        for path, (content, mode) in sorted(desired.items()):
            current = plan.inspect(path)
            if path not in old_files and current.kind != "missing":
                raise InstallError(f"Unowned file already exists: {path}; will not overwrite it")
            plan.write(path, content, mode)
        block_hash = plan_instruction(plan, source, instruction, old["instruction"] if old else None)
        manifest["providers"][provider] = {
            "files": {path: digest(value[0]) for path, value in sorted(desired.items())},
            "instruction": {"path": instruction, "block_sha256": block_hash},
        }
    plan.write(MANIFEST, (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())
    return plan


def check_state(plan: Plan, relative: str) -> None:
    # Check every parent, so a symlink replacing an ancestor is never followed intentionally.
    parts = relative_path(relative).split("/")
    for index in range(1, len(parts)):
        current = state(plan.project / "/".join(parts[:index]))
        if current.kind not in ("directory", "missing"):
            raise InstallError(f"Destination parent changed: {relative}")
    if state(plan.project / relative) != plan.expected[relative]:
        raise InstallError(f"Destination changed after preview: {relative}; rerun the installer")


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".codeden-skills-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def apply_plan(plan: Plan) -> None:
    if not plan.writes:
        return
    project_root(plan.project)
    for relative in plan.expected:
        check_state(plan, relative)
    lock = plan.project / LOCK
    created_dirs: list[Path] = []
    completed: list[Write] = []
    try:
        with lock.open("x", encoding="utf-8") as handle:
            handle.write(f"pid={os.getpid()}\n")
    except FileExistsError as error:
        raise InstallError(f"An installation is already active: {LOCK}") from error
    try:
        for change in plan.writes:
            # State may have changed since the initial preflight; never overwrite it.
            check_state(plan, change.path)
            destination = plan.project / change.path
            pending = []
            parent = destination.parent
            while parent != plan.project:
                if state(parent).kind == "missing":
                    pending.append(parent)
                parent = parent.parent
            for directory in reversed(pending):
                directory.mkdir()
                created_dirs.append(directory)
            atomic_write(destination, change.data, change.mode)
            completed.append(change)
    except Exception as error:
        unresolved = []
        for change in reversed(completed):
            path = plan.project / change.path
            try:
                current = state(path)
                if current.kind != "file" or current.data != change.data:
                    unresolved.append(change.path)
                    continue
                previous = plan.expected[change.path]
                if previous.kind == "missing":
                    path.unlink()
                else:
                    atomic_write(path, previous.data, previous.mode)
            except (OSError, InstallError):
                unresolved.append(change.path)
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        detail = f"; could not roll back concurrently changed paths: {', '.join(unresolved)}" if unresolved else "; written files were rolled back"
        raise InstallError(f"Installation stopped: {error}{detail}") from error
    finally:
        lock.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="Existing project directory, separate from this distribution")
    parser.add_argument("--provider", choices=("both", "codex", "claude"), default="both")
    parser.add_argument("--apply", action="store_true", help="Apply the preview; otherwise change nothing")
    args = parser.parse_args(argv)
    providers = tuple(PROVIDERS) if args.provider == "both" else (args.provider,)
    try:
        plan = make_plan(Path(__file__).absolute().parents[1], args.project, providers)
        if not plan.writes:
            print("Already up to date. No files changed.")
            return 0
        print(f"{'Apply' if args.apply else 'Dry run'}: {len(plan.writes)} file(s)")
        for change in plan.writes:
            action = "create" if plan.expected[change.path].kind == "missing" else "update"
            print(f"  {action}: {change.path}")
        if args.apply:
            apply_plan(plan)
            print("Installed project skills and routing instructions.")
            print("Review and commit these project files before starting new CodeDen factory worktrees.")
        else:
            print("No files changed. Repeat with --apply to install this preview.")
        return 0
    except (InstallError, OSError) as error:
        print(f"Install refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
