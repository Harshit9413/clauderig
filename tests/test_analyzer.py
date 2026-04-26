import json
from pathlib import Path
import pytest
from clauderig.analyzer import detect_stack


def test_detect_django(tmp_path):
    (tmp_path / "manage.py").write_text("# django")
    assert detect_stack(tmp_path) == "python-django"


def test_detect_fastapi_via_requirements(tmp_path):
    (tmp_path / "requirements.txt").write_text("fastapi>=0.100\nuvicorn\n")
    assert detect_stack(tmp_path) == "python-fastapi"


def test_detect_fastapi_via_pyproject(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.poetry.dependencies]\nfastapi = "*"\n'
    )
    assert detect_stack(tmp_path) == "python-fastapi"


def test_detect_django_via_requirements(tmp_path):
    (tmp_path / "requirements.txt").write_text("django>=4.0\ndjangorestframework\n")
    assert detect_stack(tmp_path) == "python-django"


def test_detect_php(tmp_path):
    (tmp_path / "composer.json").write_text('{"require": {}}')
    assert detect_stack(tmp_path) == "php"


def test_detect_react_web(tmp_path):
    pkg = {"dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    assert detect_stack(tmp_path) == "react-web"


def test_detect_react_native(tmp_path):
    (tmp_path / "app.json").write_text(json.dumps({"expo": {"name": "MyApp"}}))
    assert detect_stack(tmp_path) == "react-native"


def test_detect_unknown(tmp_path):
    assert detect_stack(tmp_path) is None


def test_django_manage_py_beats_requirements(tmp_path):
    (tmp_path / "manage.py").write_text("# django")
    (tmp_path / "requirements.txt").write_text("fastapi\n")
    assert detect_stack(tmp_path) == "python-django"


def test_react_native_app_json_beats_package_json(tmp_path):
    (tmp_path / "app.json").write_text(json.dumps({"expo": {"name": "App"}}))
    pkg = {"dependencies": {"react": "^18.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    assert detect_stack(tmp_path) == "react-native"


def test_invalid_app_json_returns_none(tmp_path):
    (tmp_path / "app.json").write_text("not valid json {{{")
    assert detect_stack(tmp_path) is None


def test_invalid_package_json_returns_none(tmp_path):
    (tmp_path / "package.json").write_text("not valid json {{{")
    assert detect_stack(tmp_path) is None


def test_php_beats_django_via_requirements(tmp_path):
    (tmp_path / "composer.json").write_text('{"require": {}}')
    (tmp_path / "requirements.txt").write_text("django>=4.0\n")
    assert detect_stack(tmp_path) == "php"
