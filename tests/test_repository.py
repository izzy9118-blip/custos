from pathlib import Path
from custos.validation import validate_repository

def root() -> Path:
    return Path(__file__).resolve().parents[1]

def test_cold_start_has_one_active_instruction():
    r=root()
    assert (r/"CUSTOS.md").is_file()
    assert list(r.glob("**/*Project_Instructions*")) == []
    assert list(r.glob("**/*Codex_Amendment*")) == []

def test_repository_validates():
    result=validate_repository(root())
    assert result["valid"] is True
    assert result["stages"] == 5
    assert result["techniques"] == 22
    assert len(result["evidence"]) == 2
