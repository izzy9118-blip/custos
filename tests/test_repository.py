from pathlib import Path

from custos.config import load_config
from custos.validation import validate_repository


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_cold_start_has_one_active_instruction():
    repository = root()
    assert (repository / "CUSTOS.md").is_file()
    assert list(repository.glob("**/*Project_Instructions*")) == []
    assert list(repository.glob("**/*Codex_Amendment*")) == []


def test_repository_has_no_global_active_inquiry():
    config = load_config(root())
    assert "active_inquiry" not in config
    assert "defaults" not in config
    assert config["inquiries_root"] == "inquiries"


def test_repository_validates_without_selecting_an_inquiry():
    result = validate_repository(root())
    assert result["valid"] is True
    assert result["stages"] == 5
    assert result["techniques"] == 22
    assert result["roots"]["inquiries"] == "inquiries"
