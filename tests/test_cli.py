"""Unit tests for q4s CLI tool."""

import subprocess
import sys
import unittest
from io import StringIO

from quarto4sbp.cli import cmd_echo, cmd_help, main


class TestCmdHelp(unittest.TestCase):
    """Tests for cmd_help function."""

    def test_help_returns_zero(self) -> None:
        """Test that help command returns exit code 0."""
        result = cmd_help()
        self.assertEqual(result, 0)

    def test_help_output(self) -> None:
        """Test that help command outputs expected content."""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            _ = cmd_help()
            output = sys.stdout.getvalue()

            # Check for key content
            self.assertIn("q4s", output)
            self.assertIn("help", output)
            self.assertIn("echo", output)
            self.assertIn("Usage:", output)
        finally:
            sys.stdout = old_stdout


class TestCmdEcho(unittest.TestCase):
    """Tests for cmd_echo function."""

    def test_echo_empty_args(self) -> None:
        """Test echo with no arguments."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = cmd_echo([])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertEqual(output.strip(), "")
        finally:
            sys.stdout = old_stdout

    def test_echo_single_arg(self) -> None:
        """Test echo with single argument."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = cmd_echo(["hello"])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertEqual(output.strip(), "hello")
        finally:
            sys.stdout = old_stdout

    def test_echo_multiple_args(self) -> None:
        """Test echo with multiple arguments."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = cmd_echo(["hello", "world", "test"])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertEqual(output.strip(), "hello world test")
        finally:
            sys.stdout = old_stdout


class TestMain(unittest.TestCase):
    """Tests for main function."""

    def test_no_args_shows_help(self) -> None:
        """Test that no arguments defaults to help."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = main([])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertIn("q4s", output)
            self.assertIn("help", output)
        finally:
            sys.stdout = old_stdout

    def test_help_command(self) -> None:
        """Test explicit help command."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = main(["help"])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertIn("q4s", output)
        finally:
            sys.stdout = old_stdout

    def test_echo_command(self) -> None:
        """Test echo command with arguments."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = main(["echo", "hello", "world"])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertEqual(output.strip(), "hello world")
        finally:
            sys.stdout = old_stdout

    def test_echo_no_args(self) -> None:
        """Test echo command with no arguments."""
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            result = main(["echo"])
            output = sys.stdout.getvalue()

            self.assertEqual(result, 0)
            self.assertEqual(output.strip(), "")
        finally:
            sys.stdout = old_stdout

    def test_invalid_command(self) -> None:
        """Test invalid command returns error."""
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            result = main(["invalid"])
            error = sys.stderr.getvalue()

            self.assertEqual(result, 1)
            self.assertIn("Unknown command", error)
            self.assertIn("invalid", error)
        finally:
            sys.stderr = old_stderr


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for the q4s CLI."""

    def test_cli_help(self) -> None:
        """Test CLI help via subprocess."""
        result = subprocess.run(
            ["uv", "run", "q4s", "help"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("q4s", result.stdout)
        self.assertIn("help", result.stdout)
        self.assertIn("echo", result.stdout)

    def test_cli_echo(self) -> None:
        """Test CLI echo via subprocess."""
        result = subprocess.run(
            ["uv", "run", "q4s", "echo", "hello", "world"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "hello world")

    def test_cli_invalid_command(self) -> None:
        """Test CLI with invalid command via subprocess."""
        result = subprocess.run(
            ["uv", "run", "q4s", "invalid"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Unknown command", result.stderr)


if __name__ == "__main__":
    unittest.main()
