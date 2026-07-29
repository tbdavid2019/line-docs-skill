from __future__ import annotations

import subprocess
from pathlib import Path


def run(
    *args: str,
    cwd: Path,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=check,
        env=env,
        text=True,
        capture_output=True,
    )


def init_git_repository(path: Path) -> None:
    path.mkdir(parents=True)
    run("git", "init", "-b", "main", cwd=path)
    run("git", "config", "user.name", "Test User", cwd=path)
    run("git", "config", "user.email", "test@example.com", cwd=path)


def commit_all(path: Path, message: str) -> str:
    run("git", "add", ".", cwd=path)
    run("git", "commit", "-m", message, cwd=path)
    return run("git", "rev-parse", "HEAD", cwd=path).stdout.strip()
