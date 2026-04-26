from pathlib import Path
from typer.testing import CliRunner
from clauderig.cli import app
from clauderig import __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.output.strip() == f"clauderig {__version__}"


def test_list_shows_all_stacks():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "FastAPI" in result.output
    assert "Django" in result.output
    assert "Laravel" in result.output
    assert "ReactJS" in result.output
    assert "React Native" in result.output


def test_init_dry_run(tmp_path):
    result = runner.invoke(app, [
        "init", "--lang", "python", "--framework", "fastapi",
        "--target", str(tmp_path), "--dry-run",
    ])
    assert result.exit_code == 0
    assert not (tmp_path / ".claude").exists()
    assert "would copy" in result.output


def test_init_noninteractive_fastapi(tmp_path):
    result = runner.invoke(app, [
        "init", "--lang", "python", "--framework", "fastapi",
        "--target", str(tmp_path),
    ])
    assert result.exit_code == 0
    assert (tmp_path / ".claude").is_dir()
    assert "Copied .claude/ to" in result.output
    assert "commands" in result.output
    assert result.output.count("→") == 2


def test_init_php_no_framework(tmp_path):
    result = runner.invoke(app, ["init", "--lang", "php", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".claude").is_dir()


def test_init_invalid_framework_for_php():
    result = runner.invoke(app, ["init", "--lang", "php", "--framework", "fastapi", "--target", "/tmp"])
    assert result.exit_code == 1


def test_init_missing_framework_for_python():
    result = runner.invoke(app, ["init", "--lang", "python", "--target", "/tmp"])
    assert result.exit_code == 1


def test_init_existing_without_force(tmp_path):
    runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi", "--target", str(tmp_path)])
    result = runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "--force" in result.output


def test_init_force_overwrites(tmp_path):
    runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi", "--target", str(tmp_path)])
    result = runner.invoke(app, [
        "init", "--lang", "python", "--framework", "fastapi",
        "--target", str(tmp_path), "--force",
    ])
    assert result.exit_code == 0


def test_all_stacks_noninteractive(tmp_path):
    combos = [
        (["--lang", "python", "--framework", "django"], "python-django"),
        (["--lang", "react", "--framework", "reactjs"], "react-web"),
        (["--lang", "react", "--framework", "react-native"], "react-native"),
    ]
    for i, (flags, _) in enumerate(combos):
        target = tmp_path / str(i)
        target.mkdir()
        result = runner.invoke(app, ["init"] + flags + ["--target", str(target)])
        assert result.exit_code == 0, f"Failed: {flags}\n{result.output}"
