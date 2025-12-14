"""Command to create a new Quarto PowerPoint presentation from template."""

import sys

from quarto4sbp.utils.scaffolding import create_quarto_project


def cmd_new_pptx(args: list[str]) -> int:
    """Create a new Quarto PowerPoint presentation from template.

    Args:
        args: Command-line arguments (should contain directory name)

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    if len(args) == 0:
        print("Error: Directory name required", file=sys.stderr)
        print("Usage: q4s new-pptx <directory>", file=sys.stderr)
        return 1

    return create_quarto_project(
        dir_name=args[0],
        qmd_template_name="simple-presentation.qmd",
        output_type="PowerPoint (.pptx)",
        templates={"simple-presentation.pptx": "simple-presentation.pptx"},
    )
