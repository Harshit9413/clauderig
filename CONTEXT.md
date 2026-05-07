# clauderig — Architecture Decisions

## Why Zip-Based Template Bundling (Not `datas`)

PyInstaller's `datas` mechanism extracts files to `sys._MEIPASS` at runtime, creating a temp directory
whose path differs between macOS and Linux. Early versions of clauderig used `datas` and hit two problems:

1. **Path inconsistency**: `sys._MEIPASS` paths use OS-native separators; our `Path`-based resolver
   produced subtle mismatches on Linux CI.
2. **Extraction overhead**: Large template trees (multiple `.claude/` trees) added noticeable startup
   latency as PyInstaller extracted them on each run.

The fix: templates are pre-zipped into `templates_bundle.zip` at build time and embedded as a single
binary blob. At runtime, `_template_src()` in `installer.py` reads directly from the zip via
`zipfile.ZipFile` — no extraction needed. The frozen path is deterministic and startup is fast.

## Why PyInstaller for Distribution

The target audience installs clauderig as a **tool**, not a library — many users don't have Python on
PATH or manage multiple Python versions. Alternatives considered:

| Option | Rejected Because |
|--------|-----------------|
| `pip install` | Requires Python + pip; version conflicts with user's own projects |
| Docker | Too heavy for a CLI utility |
| Homebrew formula | Extra maintenance burden; delays releases |
| `pipx` | Still requires Python; less universal |

PyInstaller produces a single self-contained binary for macOS (arm64) and Linux (x86_64) with no
runtime dependencies. CI publishes binaries to GitHub Releases via `.github/workflows/release.yml`.

## Release Workflow Decisions

- **Two binaries per release**: `clauderig_<version>_macos_arm64.zip` and a Linux counterpart.
  macOS binary is built on the dev machine (`build-macos.sh`); Linux is built in GitHub Actions
  (`build-linux.sh`).
- **No fat/universal binaries**: macOS arm64 only (M1+). Intel macOS users use `pip install clauderig`.
- **Version source of truth**: `pyproject.toml` `[project] version`. `__init__.py` reads it via
  `importlib.metadata.version("clauderig")` — no duplication across files.
- **GPG signing**: `clauderig.gpg` signs the release zip. Verification instructions are in `install.sh`.
- **install.sh**: Curl-installable bootstrap that detects OS/arch, downloads the correct binary, and
  places it on PATH.
