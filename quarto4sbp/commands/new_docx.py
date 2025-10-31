"""Command to create a new Quarto Word document from template."""

import sys

from quarto4sbp.utils.scaffolding import create_quarto_project


def cmd_new_docx(args: list[str]) -> int:
    """Create a new Quarto Word document from template.

    Args:
        args: Command-line arguments (should contain directory name)

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    if len(args) == 0:
        print("Error: Directory name required", file=sys.stderr)
        print("Usage: q4s new-docx <directory>", file=sys.stderr)
        return 1

    return create_quarto_project(
        dir_name=args[0],
        qmd_template_name="simple-document.qmd",
        output_type="Word (.docx)",
        templates={"simple-document.docx": "simple-document.docx"},
    )
