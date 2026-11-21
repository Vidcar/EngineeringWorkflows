#!/usr/bin/env python3
"""Read-only Git snapshot including tracked, dirty and untracked non-ignored files."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def capture(repo, base="HEAD"):
    # Remove Git's line terminator, preserving whitespace in the actual path.
    repo = Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel").removesuffix(b"\n"))).resolve()
    head = git(repo, "rev-parse", "--verify", "HEAD^{commit}").decode().strip()
    base_sha = git(repo, "rev-parse", "--verify", base + "^{commit}").decode().strip()
    paths = set(git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")) - {b""}
    files = []
    for raw in sorted(paths):
        name = os.fsdecode(raw)
        p = repo / name
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe Git path: {name}")
        for parent in p.parents:
            if parent == repo:
                break
            if parent.is_symlink():
                raise ValueError(f"Parent symlink prevents safe snapshot: {name}")
        if p.is_symlink():
            value, kind = os.fsencode(os.readlink(p)), "symlink"
        elif not p.exists():
            value, kind = b"", "deleted"
        elif p.is_file():
            value, kind = p.read_bytes(), "file"
        else:
            raise ValueError(f"Unsupported tracked entry {name}; identify submodule/runtime content separately")
        files.append({"path": name, "kind": kind, "sha256": hashlib.sha256(value).hexdigest(),
                      "executable": bool(p.lstat().st_mode & 0o111) if p.exists() or p.is_symlink() else False})
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
