from __future__ import annotations
from pathlib import Path
import argparse, json
from datetime import datetime, timezone
from .config import find_repo_root, load_config
from .validation import validate_repository
from .runner import analyze, sanctum_report

def build_parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="custos")
    p.add_argument("--repo-root")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("validate")
    sub.add_parser("show")
    a=sub.add_parser("analyze")
    a.add_argument("--output")
    a.add_argument("--reasoner-command")
    s=sub.add_parser("sanctum-report")
    s.add_argument("--envelope",required=True)
    s.add_argument("--output",required=True)
    return p

def main() -> int:
    args=build_parser().parse_args()
    root=find_repo_root(Path(args.repo_root) if args.repo_root else None)
    if args.command=="validate":
        print(json.dumps(validate_repository(root),indent=2)); return 0
    if args.command=="show":
        cfg=load_config(root); inquiry=root/cfg["active_inquiry"]
        print((inquiry/"inquiry.md").read_text(encoding="utf-8")); return 0
    if args.command=="analyze":
        cfg=load_config(root)
        default=root/cfg["runs_root"]/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
        print(analyze(root,Path(args.output).resolve() if args.output else default,args.reasoner_command)); return 0
    if args.command=="sanctum-report":
        print(sanctum_report(root,Path(args.envelope),Path(args.output))); return 0
    raise AssertionError(args.command)

if __name__ == "__main__":
    raise SystemExit(main())
