from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import json

from .config import find_repo_root, load_config
from .runner import READER_MODES, execute_reader, prepare_reader, sanctum_report
from .validation import validate_inquiry, validate_repository


def _add_reader_input(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source", help="UTF-8 source witness to open or sweep")
    group.add_argument("--inquiry", help="Registered inquiry directory to resume")
    parser.add_argument("--mode", choices=READER_MODES, required=True)
    parser.add_argument("--output")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="custos")
    parser.add_argument("--repo-root")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--inquiry")

    show = sub.add_parser("show")
    show.add_argument("--inquiry", required=True)

    prepare = sub.add_parser("prepare", help="Build a Reader request without claiming analysis")
    _add_reader_input(prepare)

    read = sub.add_parser("read", help="Execute substantive Strauss Reader analysis")
    _add_reader_input(read)
    read.add_argument("--reasoner-command", required=True)

    sanctum = sub.add_parser("sanctum-report")
    sanctum.add_argument("--inquiry", required=True)
    sanctum.add_argument("--envelope", required=True)
    sanctum.add_argument("--output", required=True)
    return parser


def _reader_paths(args: argparse.Namespace) -> tuple[Path | None, Path | None]:
    source = Path(args.source).expanduser().resolve() if args.source else None
    inquiry = Path(args.inquiry) if args.inquiry else None
    return source, inquiry


def main() -> int:
    args = build_parser().parse_args()
    root = find_repo_root(Path(args.repo_root) if args.repo_root else None)

    if args.command == "validate":
        print(json.dumps(validate_repository(root, inquiry=args.inquiry), indent=2))
        return 0

    if args.command == "show":
        checked = validate_inquiry(root, args.inquiry)
        print((root / checked["path"] / "inquiry.md").read_text(encoding="utf-8"))
        return 0

    if args.command in {"prepare", "read"}:
        config = load_config(root)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        default = root / config["runs_root"] / f"{timestamp}-{args.mode}"
        output = Path(args.output).expanduser().resolve() if args.output else default
        source, inquiry = _reader_paths(args)
        if args.command == "prepare":
            result = prepare_reader(
                root, output, mode=args.mode, source=source, inquiry=inquiry
            )
        else:
            result = execute_reader(
                root,
                output,
                mode=args.mode,
                reasoner_command=args.reasoner_command,
                source=source,
                inquiry=inquiry,
            )
        print(result)
        return 0

    if args.command == "sanctum-report":
        print(
            sanctum_report(
                root, Path(args.inquiry), Path(args.envelope), Path(args.output)
            )
        )
        return 0

    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
