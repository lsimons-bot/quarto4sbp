# 002 - q4s CLI Tool

**Purpose:** Create a simple CLI tool called `q4s` (quarto4sbp) with basic help and echo subcommands as a foundation for future functionality

**Requirements:**
- Executable CLI tool named `q4s`
- `q4s help` subcommand to display usage information
- `q4s echo [args...]` subcommand to echo back command-line arguments
- Follow dependency-free core philosophy (stdlib only: argparse, sys)
- Proper exit codes (0 for success, 1 for errors)
- Type hints for all functions
- Unit tests for both subcommands

**Design Approach:**
- Main entry point: `quarto4sbp/cli.py` with `main()` function
- Use argparse with subparsers for extensibility
- `help` command shows available subcommands and usage
- `echo` command prints all arguments separated by spaces
- Install as console script via pyproject.toml

**File Structure:**
```
quarto4sbp/
  cli.py          # Main CLI entry point with argparse setup
tests/
  test_cli.py     # Unit tests for help and echo commands
```

**API Design:**
- `main(args: list[str] | None = None) -> int` - Entry point, returns exit code
- `cmd_help() -> int` - Handle help subcommand
- `cmd_echo(args: list[str]) -> int` - Handle echo subcommand

**Testing Strategy:**
- Test help output includes "q4s" and "help", "echo" commands
- Test echo with zero, one, and multiple arguments
- Test unknown subcommand returns exit code 1
- Use subprocess for integration testing of installed CLI

**Implementation Notes:**
- Follow shared patterns from `000-shared-patterns.md`
- No external dependencies beyond stdlib
- Simple, extensible design for future subcommands

**Status:** Implemented