from __future__ import annotations

import subprocess
from pathlib import Path


class GitReadError(RuntimeError):
    pass


class LocalGitReader:
    """Read a local repository only through an explicitly declared commit."""

    def __init__(self, repo_root: Path, git_commit: str) -> None:
        self.repo_root = repo_root.expanduser().resolve()
        self.git_commit = git_commit
        if not (self.repo_root / ".git").exists():
            raise GitReadError(f"Not a Git repository: {self.repo_root}")
        self._run_git("cat-file", "-e", f"{self.git_commit}^{{commit}}")
        self.resolved_commit = self._run_git(
            "rev-parse", f"{self.git_commit}^{{commit}}"
        ).strip()

    def _run_git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip()
            raise GitReadError(message or f"Git command failed: {args}")
        return result.stdout

    def read_text(self, repository_path: str) -> str:
        self._validate_path(repository_path)
        return self._run_git("show", f"{self.resolved_commit}:{repository_path}")

    def list_files(self, prefix: str = "") -> list[str]:
        if prefix:
            self._validate_path(prefix)
        output = self._run_git(
            "ls-tree", "-r", "--name-only", self.resolved_commit, "--", prefix
        )
        return sorted(line for line in output.splitlines() if line)

    def file_exists(self, repository_path: str) -> bool:
        self._validate_path(repository_path)
        result = subprocess.run(
            [
                "git", "-C", str(self.repo_root),
                "cat-file", "-e",
                f"{self.resolved_commit}:{repository_path}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    @staticmethod
    def _validate_path(repository_path: str) -> None:
        path = Path(repository_path)
        if path.is_absolute() or ".." in path.parts:
            raise GitReadError("Repository path must be relative and non-traversing")
