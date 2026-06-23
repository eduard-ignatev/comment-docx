from pathlib import Path

from click.testing import CliRunner

from comment_docx import cli as cli_module
from comment_docx.commenter import CommentDocxError, CommentResult


def test_cli_add_reports_output(monkeypatch, tmp_path: Path) -> None:
    input_path = tmp_path / "sample.docx"
    input_path.write_bytes(b"placeholder")
    output_path = tmp_path / "sample.commented.docx"
    captured = {}

    monkeypatch.setenv("PROVIDER_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("PROVIDER_API_KEY", "test-key")
    monkeypatch.setenv("PROVIDER_MODEL", "test-model")

    def fake_add_comments_to_docx(**kwargs) -> CommentResult:
        captured.update(kwargs)
        return CommentResult(
            input_path=input_path,
            output_path=kwargs["output_path"],
            match_count=2,
            run_count=5,
        )

    monkeypatch.setattr(cli_module, "add_comments_to_docx", fake_add_comments_to_docx)

    result = CliRunner().invoke(cli_module.cli, ["add", str(input_path), "Find unclear text"])

    assert result.exit_code == 0
    assert captured["output_path"] == output_path
    assert captured["query"] == "Find unclear text"
    assert "Output: " in result.output
    assert "Comments: 2" in result.output
    assert "Runs: 5" in result.output


def test_cli_add_uses_explicit_provider_options(monkeypatch, tmp_path: Path) -> None:
    input_path = tmp_path / "sample.docx"
    input_path.write_bytes(b"placeholder")
    captured = {}

    def fake_add_comments_to_docx(**kwargs) -> CommentResult:
        captured.update(kwargs)
        return CommentResult(
            input_path=input_path,
            output_path=kwargs["output_path"],
            match_count=0,
            run_count=1,
        )

    monkeypatch.setattr(cli_module, "add_comments_to_docx", fake_add_comments_to_docx)

    result = CliRunner().invoke(
        cli_module.cli,
        [
            "add",
            str(input_path),
            "Find unclear text",
            "--provider-base-url",
            "https://example.com/v1",
            "--api-key",
            "test-key",
            "--model",
            "test-model",
        ],
    )

    assert result.exit_code == 0
    assert captured["provider"].base_url == "https://example.com/v1"
    assert captured["provider"].api_key == "test-key"
    assert captured["provider"].model == "test-model"


def test_cli_add_reports_missing_provider_config(monkeypatch, tmp_path: Path) -> None:
    input_path = tmp_path / "sample.docx"
    input_path.write_bytes(b"placeholder")
    monkeypatch.delenv("PROVIDER_BASE_URL", raising=False)
    monkeypatch.delenv("PROVIDER_API_KEY", raising=False)
    monkeypatch.delenv("PROVIDER_MODEL", raising=False)
    monkeypatch.setattr(cli_module, "load_dotenv", lambda: None)

    result = CliRunner().invoke(cli_module.cli, ["add", str(input_path), "Find unclear text"])

    assert result.exit_code == 1
    assert "Missing OpenAI-compatible provider configuration" in result.output


def test_cli_add_reports_commenting_error(monkeypatch, tmp_path: Path) -> None:
    input_path = tmp_path / "sample.docx"
    input_path.write_bytes(b"placeholder")
    monkeypatch.setenv("PROVIDER_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("PROVIDER_API_KEY", "test-key")
    monkeypatch.setenv("PROVIDER_MODEL", "test-model")

    def fake_add_comments_to_docx(**kwargs) -> CommentResult:
        raise CommentDocxError("bad model output")

    monkeypatch.setattr(cli_module, "add_comments_to_docx", fake_add_comments_to_docx)

    result = CliRunner().invoke(cli_module.cli, ["add", str(input_path), "Find unclear text"])

    assert result.exit_code == 1
    assert "Error: bad model output" in result.output
