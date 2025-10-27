"""Unified new command for creating documents with both PowerPoint and Word outputs."""

import sys
from pathlib import Path

from quarto4sbp.utils.scaffolding import (
    create_directory,
    create_qmd_file,
    create_render_script,
    create_template_symlink,
    get_template_path,
    validate_directory_name,
    verify_template_exists,
)


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

    dir_name = args[0]

    # Validate directory name
    if not validate_directory_name(dir_name):
        print(f"Error: Invalid directory name '{dir_name}'", file=sys.stderr)
        return 1

    # Get paths
    target_dir = Path(dir_name)
    base_name = target_dir.name
    qmd_file = target_dir / f"{base_name}.qmd"
    pptx_symlink = target_dir / "simple-presentation.pptx"
    docx_symlink = target_dir / "simple-document.docx"
    render_script = target_dir / "render.sh"

    # Get template paths
    template_pptx = get_template_path("simple-presentation.pptx")
    template_docx = get_template_path("simple-document.docx")
    template_render = get_template_path("render.sh.template")
    template_qmd = get_template_path("combined-document.qmd")

    # Verify templates exist
    if not verify_template_exists(template_pptx, "PowerPoint template"):
        return 1
    if not verify_template_exists(template_docx, "Word template"):
        return 1
    if not verify_template_exists(template_render, "Render script template"):
        return 1
    if not verify_template_exists(template_qmd, "QMD template"):
        return 1

    # Create directory if it doesn't exist
    if not create_directory(target_dir):
        return 1

    # Create QMD file from template
    if not create_qmd_file(qmd_file, template_qmd, base_name):
        return 1

    # Create render.sh script from template
    if not create_render_script(render_script, template_render, base_name):
        return 1

    # Create symlinks to both templates
    created_symlinks: list[str] = []

    # PowerPoint symlink
    if create_template_symlink(pptx_symlink, template_pptx, target_dir, "PowerPoint"):
        created_symlinks.append("PowerPoint")

    # Word symlink
    if create_template_symlink(docx_symlink, template_docx, target_dir, "Word"):
        created_symlinks.append("Word")

    # Success output
    print(f"Created: {qmd_file}")
    print("Outputs: Both PowerPoint (.pptx) and Word (.docx)")
    print(f"Hint: Run 'cd {target_dir} && ./render.sh' to generate both formats")

    return 0
