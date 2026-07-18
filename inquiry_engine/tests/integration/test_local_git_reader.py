import shutil
import subprocess
from pathlib import Path

import pytest

from custos_engine.repository.github_reader import LocalGitReader


@pytest.mark.skipif(shutil.which("git") is None, reason="git executable unavailable")
def test_reader_is_pinned_to_declared_commit(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "test@example.com"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.name", "Test"],
        check=True,
    )

    file_path = repo / "artifact.txt"
    file_path.write_text("first\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "artifact.txt"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "first"], check=True)
    first_commit = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    file_path.write_text("second\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-am", "second"], check=True)

    reader = LocalGitReader(repo, first_commit)
    assert reader.read_text("artifact.txt") == "first\n"
