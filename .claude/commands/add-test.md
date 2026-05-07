---
name: add-test
description: Write a pytest test for a clauderig CLI command, installer function, or analyzer function.
---

# /add-test

Ask the user:
1. What to test? (CLI command, `installer.py` function, or `analyzer.py` function)
2. What behavior should the test verify?
3. Does it need real filesystem access or can signals be simulated in `tmp_path`?

Then:
- Find the function to test in `src/clauderig/`
- Write a focused test in `tests/test_<module>.py`
- For CLI commands: use `typer.testing.CliRunner` from `typer.testing`
- For `installer.py`: use `tmp_path` fixture; build real directory structures
- For `analyzer.py`: create signal files (e.g., `requirements.txt`, `package.json`) in `tmp_path`
- Name tests: `test_<what>_<expected_outcome>` (e.g., `test_install_creates_claude_dir`)

Example for analyzer:
```python
def test_detect_stack_fastapi(tmp_path):
    (tmp_path / "requirements.txt").write_text("fastapi>=0.100\n")
    assert detect_stack(tmp_path) == "python-fastapi"
```

Example for CLI:
```python
from typer.testing import CliRunner
from clauderig.cli import app

def test_init_dry_run(tmp_path):
    result = CliRunner().invoke(app, ["init", "--lang", "python",
                                      "--framework", "fastapi",
                                      "--target", str(tmp_path), "--dry-run"])
    assert result.exit_code == 0
```

Run `pytest -xvs tests/<test_file>.py::<test_name>` and show output.
