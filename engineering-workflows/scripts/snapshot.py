#!/usr/bin/env python3
"""Read-only Git snapshot including tracked, dirty and untracked non-ignored files."""
import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


WINDOWS_RESERVED_CHARACTERS = set('<>:"\\|?*') | {chr(code) for code in range(32)}
WINDOWS_RESERVED_DEVICES = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {
    prefix + digit for prefix in ("COM", "LPT") for digit in "123456789\u00b9\u00b2\u00b3"
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def worktree_stat(path, windows_names):
    info = path.lstat()
    if windows_names is not None:
        # Cache exact directory entries. WindowsPath equality folds case even
        # in directories where NTFS allows two distinct spellings.
        directory = str(path.parent)
        if directory not in windows_names:
            windows_names[directory] = {entry.name for entry in path.parent.iterdir()}
        if path.name not in windows_names[directory]:
            raise ValueError(f"Git path uses a Windows alias: {path}")
    return info


def worktree_entry(repo, name, windows_names):
    # Git paths always use forward slashes. Check the components before the
    # host has a chance to reinterpret them as separators, streams or aliases.
    parts = name.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"Unsafe Git path: {name!r}")
    windows = windows_names is not None
    if windows and any(
        part.endswith((" ", "."))
        or not WINDOWS_RESERVED_CHARACTERS.isdisjoint(part)
        or part.partition(".")[0].rstrip(" ").upper() in WINDOWS_RESERVED_DEVICES
        for part in parts
    ):
        raise ValueError(f"Unsafe Windows Git path: {name!r}")

    path = repo
    try:
        for part in parts[:-1]:
            path /= part
            parent = worktree_stat(path, windows_names)
            if stat.S_ISLNK(parent.st_mode):
                raise ValueError(f"Parent symlink prevents safe snapshot: {name!r}")
            if windows and parent.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT:
                raise ValueError(f"Parent junction prevents safe snapshot: {name!r}")
        path /= parts[-1]
        mode = worktree_stat(path, windows_names).st_mode
    except (FileNotFoundError, NotADirectoryError):
        return b"", "deleted", False

    # Windows stat synthesizes execute bits for some extensions. Git's
    # staged executable bit is captured separately in the index hash.
    executable = not windows and bool(mode & 0o111)
    if stat.S_ISLNK(mode):
        return os.fsencode(os.readlink(path)), "symlink", executable
    if stat.S_ISREG(mode):
        return path.read_bytes(), "file", executable
    raise ValueError(f"Unsupported tracked entry {name!r}. Identify submodule/runtime content separately.")


def capture(repo, base="HEAD"):
    # Remove Git's line terminator, preserving whitespace in the actual path.
    repo = Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel").removesuffix(b"\n"))).resolve()
    head = git(repo, "rev-parse", "--verify", "HEAD^{commit}").decode().strip()
    base_sha = git(repo, "rev-parse", "--verify", base + "^{commit}").decode().strip()
    paths = set(git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")) - {b""}
    windows_names = {} if os.name == "nt" else None
    files = []
    for raw in sorted(paths):
        name = os.fsdecode(raw)
        value, kind, executable = worktree_entry(repo, name, windows_names)
        files.append({"path": name, "kind": kind, "sha256": hashlib.sha256(value).hexdigest(),
                      "executable": executable})
    index_sha = hashlib.sha256(git(repo, "ls-files", "--stage", "-z")).hexdigest()
    result = {"schema_version": 1, "repository": str(repo), "base_ref": base, "base": base_sha, "head": head,
              "content_sha256": digest(files), "index_sha256": index_sha, "files": files}
    result["snapshot_id"] = digest({k: result[k] for k in ("base_ref", "base", "head", "content_sha256", "index_sha256")})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--base", default="HEAD")
    args = parser.parse_args()
    try:
        print(json.dumps(capture(args.repo, args.base), indent=2, ensure_ascii=True))
    except (OSError, ValueError, subprocess.CalledProcessError) as e:
        parser.exit(1, f"Snapshot failed: {e}\n")


if __name__ == "__main__":
    main()
