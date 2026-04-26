import json
import os
from pathlib import Path
import pytest
from clauderig.installer import install, InstallResult

STACKS = ["python-fastapi", "python-django", "php", "react-web", "react-native"]


@pytest.mark.parametrize("stack", STACKS)
def test_install_creates_claude_dir(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    assert (tmp_path / ".claude").is_dir()


@pytest.mark.parametrize("stack", STACKS)
def test_install_creates_settings_json(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    settings = tmp_path / ".claude" / "settings.json"
    assert settings.exists()
    data = json.loads(settings.read_text())
    assert "permissions" in data
    assert "mcpServers" in data


@pytest.mark.parametrize("stack", STACKS)
def test_install_creates_claude_md(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    assert (tmp_path / ".claude" / "CLAUDE.md").exists()


@pytest.mark.parametrize("stack", STACKS)
def test_install_has_at_least_one_command(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    commands = list((tmp_path / ".claude" / "commands").glob("*.md"))
    assert len(commands) >= 1


@pytest.mark.parametrize("stack", STACKS)
def test_install_has_at_least_one_skill(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    skills = list((tmp_path / ".claude" / "skills").iterdir())
    assert len(skills) >= 1


@pytest.mark.parametrize("stack", STACKS)
def test_hooks_are_executable(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    hooks_dir = tmp_path / ".claude" / "hooks"
    for sh in hooks_dir.glob("*.sh"):
        assert os.access(sh, os.X_OK), f"{sh} is not executable"


def test_install_raises_on_existing_without_force(tmp_path):
    install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    with pytest.raises(FileExistsError, match="--force"):
        install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)


def test_install_force_overwrites(tmp_path):
    install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    install(stack="python-fastapi", target=tmp_path, force=True, dry_run=False)
    assert (tmp_path / ".claude").is_dir()


def test_dry_run_does_not_create_dir(tmp_path, capsys):
    result = install(stack="python-fastapi", target=tmp_path, force=False, dry_run=True)
    assert not (tmp_path / ".claude").exists()
    assert result.commands_count == 0


def test_install_result_counts(tmp_path):
    result = install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    assert isinstance(result, InstallResult)
    assert result.commands_count >= 1
    assert result.skills_count >= 1
    assert result.hooks_count >= 1
    assert result.ruleset_count >= 1
    assert len(result.mcps_configured) >= 1
    assert result.target_path == tmp_path / ".claude"


def test_invalid_stack_raises(tmp_path):
    with pytest.raises(ValueError, match="Unknown stack"):
        install(stack="not-a-stack", target=tmp_path, force=False, dry_run=False)
