"""CLI entry point for q4s (quarto4sbp) tool."""

import argparse
import sys


def cmd_help() -> int:
    """Handle the help subcommand.

    Returns:
        Exit code (0 for success)
    """
    print("q4s - quarto4sbp CLI tool")
    print()
    print("Usage: q4s <command> [arguments]")
    print()
    print("Available commands:")
    print("  help       Show this help message")
    print("  echo       Echo back the command-line arguments")
    print()
    print("Examples:")
    print("  q4s help")
    print("  q4s echo hello world")
    return 0


def cmd_echo(args: list[str]) -> int:
    """Handle the echo subcommand.

    Args:
        args: Arguments to echo back

    Returns:
        Exit code (0 for success)
    """
    print(" ".join(args))
    return 0


def main(args: list[str] | None = None) -> int:
    """Main entry point for q4s CLI.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    parser = argparse.ArgumentParser(
        prog="q4s",
        description="quarto4sbp CLI tool",
        add_help=False,  # We handle help ourselves
    )

    parser.add_argument(
        "command",
        nargs="?",
        help="Command to run (help, echo)",
    )

    parser.add_argument(
        "command_args",
        nargs="*",
        help="Arguments for the command",
    )

    parsed = parser.parse_args(args)

    command = parsed.command
    command_args = parsed.command_args

    # Default to help if no command provided
    if command is None:
        return cmd_help()

    # Route to appropriate subcommand
    if command == "help":
        return cmd_help()
    elif command == "echo":
        return cmd_echo(command_args)
    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        print("Run 'q4s help' for usage information", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
