# 004 - Install Script with q4s Shim

**Purpose:** Provide a user-friendly install script that creates a `~/.local/bin/q4s` shim to run the CLI from the project's venv, eliminating the need to type `uv run q4s` every time

**Requirements:**
- Install script creates `~/.local/bin/q4s` executable shim
- Shim automatically activates the project venv and runs `q4s` CLI
- Shim detects the correct project directory (where it was installed from)
- Handle case where `~/.local/bin` doesn't exist (create it)
- Inform user if `~/.local/bin` is not in PATH
- Follow dependency-free core philosophy (bash script + Python stdlib)
- Proper error handling if venv doesn't exist

**Design Approach:**
- Python install script: `install.py` in project root
- Generated shim: bash wrapper that sources venv and runs CLI
- Store project path in shim at install time (not runtime lookup)
- Check for venv existence before generating shim
- Use `~/.local/bin` following XDG Base Directory conventions
- Install script is idempotent (safe to run multiple times)

**File Structure:**
```
install.py          # Install script in project root
~/.local/bin/q4s    # Generated shim (outside project)
```

**Shim Design:**
The shim will be a bash script that:
```bash
#!/bin/bash
PROJECT_DIR="/path/to/quarto4sbp"
source "$PROJECT_DIR/.venv/bin/activate"
exec python -m quarto4sbp.cli "$@"
```

**Install Script Behavior:**
- Verify current directory is the project root (has `pyproject.toml` with name="quarto4sbp")
- Check that `.venv` exists (prompt to run `uv venv` if missing)
- Create `~/.local/bin` directory if it doesn't exist
- Write shim to `~/.local/bin/q4s` with execute permissions
- Check if `~/.local/bin` is in user's PATH
- Print success message with usage instructions

**Error Cases:**
- Exit with error if not run from project root
- Exit with error if `.venv` doesn't exist (with helpful message)
- Exit with error if unable to create `~/.local/bin`
- Exit with error if unable to write shim file

**Usage:**
```bash
# From project root
python install.py

# After install, use q4s directly
q4s help
q4s echo hello world
```

**Testing Strategy:**
- Test install script with missing venv (should fail gracefully)
- Test install script creates directory if missing
- Test install script creates executable shim
- Test shim can successfully run q4s commands
- Test idempotency (running install twice works)
- Use temporary directory for tests, not actual ~/.local/bin

**Implementation Notes:**
- Install script should be simple and self-contained
- No dependencies beyond Python stdlib (pathlib, os, sys, subprocess)
- Shim stores absolute path to avoid pwd-dependent behavior
- Consider updating README.md with new install method

**Status:** Draft