#!/usr/bin/env python3
"""Bootstrap the Custos Inquiry Engine in an isolated virtual environment."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv


MINIMUM_PYTHON = (3, 11)


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _venv_cli(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "custos-inquiry.exe"
    return venv_dir / "bin" / "custos-inquiry"


def _run(command: list[object], *, cwd: Path) -> None:
    subprocess.run([str(part) for part in command], cwd=cwd, check=True)


def _ensure_full_git_history(repository_root: Path) -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip() == "true":
        print("Fetching full Git history required by commit-pinned tests")
        _run(
            ["git", "fetch", "--unshallow", "--tags", "origin"],
            cwd=repository_root,
        )


def main() -> int:
    engine_root = Path(__file__).resolve().parent
    repository_root = engine_root.parent

    parser = argparse.ArgumentParser(
        description=(
            "Create an isolated environment, install Custos dependencies, "
            "run the Inquiry Engine test suite, and verify the CLI."
        )
    )
    parser.add_argument(
        "--venv",
        type=Path,
        default=repository_root / ".venv",
        help="virtual-environment path (default: repository-root/.venv)",
    )
    parser.add_argument(
        "--neo4j",
        action="store_true",
        help="also install the optional Neo4j driver",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="install dependencies and smoke-test the CLI without running pytest",
    )
    args = parser.parse_args()

    if sys.version_info < MINIMUM_PYTHON:
        required = ".".join(str(part) for part in MINIMUM_PYTHON)
        current = ".".join(str(part) for part in sys.version_info[:3])
        parser.error(f"Python {required}+ is required; found Python {current}")

    venv_dir = args.venv.expanduser().resolve()
    python = _venv_python(venv_dir)
    if not python.exists():
        print(f"Creating virtual environment: {venv_dir}")
        venv.EnvBuilder(with_pip=True).create(venv_dir)

    extras = "dev,neo4j" if args.neo4j else "dev"
    editable_requirement = f"{engine_root}[{extras}]"
    print(f"Installing Inquiry Engine dependencies: {editable_requirement}")
    _run(
        [
            python,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "-e",
            editable_requirement,
        ],
        cwd=repository_root,
    )

    if not args.skip_tests:
        _ensure_full_git_history(repository_root)
        print("Running the complete Inquiry Engine test suite")
        _run(
            [python, "-m", "pytest", "-q", engine_root / "tests"],
            cwd=repository_root,
        )

    cli = _venv_cli(venv_dir)
    print("Verifying custos-inquiry CLI")
    _run([cli, "--help"], cwd=repository_root)

    print(f"Custos Inquiry Engine is ready: {python}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
