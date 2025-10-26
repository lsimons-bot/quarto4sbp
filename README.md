# quarto4sbp

A lightweight tool for working with quarto in Schuberg Philis Context.

## Prerequisites

- **Python 3.13+** with `uv` package manager: try `brew install uv` on mac
- [quarto](https://quarto.org/) CLI installed: try `brew install quarto` on mac

## Quick Start

* Set up a new venv with `uv venv`

## Development

### Spec-Based Development

This project follows a spec-based development approach documented in [`docs/spec/`](docs/spec/).

### Beads issue tracking

This project uses [beads (bd)](https://github.com/steveyegge/beads) for issue tracking.

To install try `brew tap steveyegge/beads && brew install bd` on mac.

### Development Guidelines
- See [CLAUDE.md](CLAUDE.md) for Claude Code-specific guidance
- See [AGENTS.md](AGENTS.md) for development guidelines and agent instructions
- See [DESIGN.md](DESIGN.md) for architectural decisions and design rationale
- Reference spec numbers in commit messages during feature implementation
- Run tests after changes: `uv run pytest`

## Testing

Unit and integration tests are located in `tests/`. Run them using:

```bash
# Full test suite (recommended)
uv run pytest

# Specific test file
uv run pytest tests/my_test_file.py

# With verbose output
uv run pytest -v
```
