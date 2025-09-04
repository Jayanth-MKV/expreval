#!/usr/bin/env python3
"""Simple version bump & tag helper.

Updates:
  * pyproject.toml [project].version
  * src/expreval/__init__.py __version__ constant
Creates:
  * Git commit "Bump version to X.Y.Z"
  * Git tag    "vX.Y.Z" with message "Release X.Y.Z"

Usage:
  python scripts/bump_version.py 1.2.3
  python scripts/bump_version.py --part patch   # auto increment
  python scripts/bump_version.py --part minor
  python scripts/bump_version.py --part major

Dry run:
  python scripts/bump_version.py 1.2.3 --dry-run

Notes:
  * Won't overwrite an existing tag.
  * Aborts if working tree has uncommitted changes (besides the bump) unless
    you pass --allow-dirty.
  * Does not push; run the printed git push commands after reviewing.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
INIT_FILE = ROOT / "src" / "expreval" / "__init__.py"

VERSION_RE = re.compile(r'^(version\s*=\s*")(?P<ver>[0-9]+\.[0-9]+\.[0-9]+)("\s*)$')
DUnder_VERSION_RE = re.compile(
    r'^(__version__\s*=\s*")(?P<ver>[0-9]+\.[0-9]+\.[0-9]+)("\s*)$'
)


def run(*cmd: str, check: bool = True) -> str:
    out = subprocess.run(cmd, check=check, capture_output=True, text=True)
    return out.stdout.strip()


def get_current_version() -> str:
    for line in PYPROJECT.read_text(encoding="utf-8").splitlines():
        m = VERSION_RE.match(line)
        if m:
            return m.group("ver")
    raise SystemExit("Could not find version in pyproject.toml")


def compute_bump(cur: str, part: str) -> str:
    major, minor, patch = map(int, cur.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"unknown part: {part}")
    return f"{major}.{minor}.{patch}"


def replace_version_in_file(path: pathlib.Path, pattern: re.Pattern, new: str) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = False
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if m:
            if m.group("ver") != new:
                lines[i] = f"{m.group(1)}{new}{m.group(3)}"
                changed = True
            break
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def ensure_clean(allow_dirty: bool) -> None:
    status = run("git", "status", "--porcelain")
    if status and not allow_dirty:
        print(status)
        raise SystemExit(
            "Working tree not clean. Commit or stash changes, or use --allow-dirty."
        )


def tag_exists(tag: str) -> bool:
    try:
        run("git", "rev-parse", "--verify", tag)
        return True
    except subprocess.CalledProcessError:
        return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Bump project version & create git tag.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("version", nargs="?", help="Target version X.Y.Z")
    g.add_argument(
        "--part",
        choices=["major", "minor", "patch"],
        help="Which part to auto-increment",
    )
    p.add_argument("-n", "--dry-run", action="store_true", help="Only show actions")
    p.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Proceed even if working tree is dirty",
    )
    args = p.parse_args(argv)

    cur = get_current_version()
    target = args.version or compute_bump(cur, args.part)

    if target == cur:
        raise SystemExit(f"Target version {target} is same as current {cur}")

    tag = f"v{target}"
    if tag_exists(tag):
        raise SystemExit(f"Tag {tag} already exists. Choose a different version.")

    ensure_clean(args.allow_dirty)

    print(f"Current version: {cur}\nNew version:     {target}")
    print("Updating files:")

    py_changed = replace_version_in_file(PYPROJECT, VERSION_RE, target)
    init_changed = replace_version_in_file(INIT_FILE, DUnder_VERSION_RE, target)

    if not (py_changed or init_changed):
        raise SystemExit("No version markers updated; aborting.")

    if args.dry_run:
        print("(dry-run) Would git add/commit/tag")
        return 0

    run("git", "add", str(PYPROJECT), str(INIT_FILE))
    run("git", "commit", "-m", f"Bump version to {target}")
    run("git", "tag", tag, "-m", f"Release {target}")

    print("Done.")
    print("Next push:")
    print("  git push origin HEAD")
    print(f"  git push origin {tag}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
