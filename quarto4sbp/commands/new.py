"""Unified new command for creating documents with both PowerPoint and Word outputs."""

import sys

from quarto4sbp.utils.scaffolding import create_quarto_project


def cmd_new(args: list[str]) -> int:
    """Create a new Quarto document with both PowerPoint and Word outputs.

    Creates a single .qmd file configured to output to both .pptx and .docx formats.

    Args:
        args: Command-line arguments (should contain directory name)

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    if len(args) == 0:
        print("Error: Directory name required", file=sys.stderr)
        print("Usage: q4s new <directory>", file=sys.stderr)
        return 1

    return create_quarto_project(
        dir_name=args[0],
        qmd_template_name="combined-document.qmd",
        output_type="Both PowerPoint (.pptx) and Word (.docx)",
        templates={
            "simple-presentation.pptx": "simple-presentation.pptx",
            "simple-document.docx": "simple-document.docx",
        },
    )
