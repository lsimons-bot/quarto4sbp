"""Utilities for scaffolding new Quarto projects from templates."""

import os
import sys
from pathlib import Path


def validate_directory_name(dir_name: str) -> bool:
    """Validate that a directory name is acceptable.

    Args:
        dir_name: Directory name to validate

    Returns:
        True if valid, False otherwise
    """
    return bool(dir_name and not dir_name.startswith("-"))


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path to project root (parent of quarto4sbp package)
    """
    # quarto4sbp/utils/scaffolding.py -> quarto4sbp -> project root
    return Path(__file__).parent.parent.parent


def get_template_path(template_name: str) -> Path:
    """Get the full path to a template file.

    Args:
        template_name: Name of the template file

    Returns:
        Full path to the template file
    """
    return get_project_root() / "templates" / template_name


def verify_template_exists(template_path: Path, template_type: str) -> bool:
    """Verify that a template file exists.

    Args:
        template_path: Path to template file
        template_type: Human-readable template type (e.g., "QMD template", "PowerPoint template")

    Returns:
        True if exists, False otherwise (prints error message)
    """
    if not template_path.exists():
        print(f"Error: {template_type} not found at {template_path}", file=sys.stderr)
        return False
    return True


def create_directory(target_dir: Path) -> bool:
    """Create target directory if it doesn't exist.

    Args:
        target_dir: Directory to create

    Returns:
        True if successful, False otherwise (prints error message)
    """
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        return True
    except OSError as e:
        print(f"Error: Could not create directory '{target_dir}': {e}", file=sys.stderr)
        return False


def create_qmd_file(qmd_file: Path, template_qmd: Path, base_name: str) -> bool:
    """Create a QMD file from template with title substitution.

    Args:
        qmd_file: Path where QMD file should be created
        template_qmd: Path to QMD template
        base_name: Project name to substitute for {{TITLE}}

    Returns:
        True if successful, False otherwise (prints error message)
    """
    # Check if qmd file already exists
    if qmd_file.exists():
        print(f"Error: File already exists: {qmd_file}", file=sys.stderr)
        return False

    # Load and customize QMD template
    try:
        qmd_content = template_qmd.read_text()
        qmd_content = qmd_content.replace("{{TITLE}}", base_name)
    except OSError as e:
        print(
            f"Error: Could not read QMD template '{template_qmd}': {e}", file=sys.stderr
        )
        return False

    # Write QMD file
    try:
        qmd_file.write_text(qmd_content)
        return True
    except OSError as e:
        print(f"Error: Could not create file '{qmd_file}': {e}", file=sys.stderr)
        return False


def create_render_script(
    render_script: Path, template_render: Path, base_name: str
) -> bool:
    """Create render.sh script from template.

    Args:
        render_script: Path where render script should be created
        template_render: Path to render script template
        base_name: File name to substitute for {{FILE_NAME}}

    Returns:
        True if successful, False otherwise (prints error message)
    """
    try:
        render_content = template_render.read_text()
        render_content = render_content.replace("{{FILE_NAME}}", base_name)
        render_script.write_text(render_content)
        render_script.chmod(0o755)
        return True
    except OSError as e:
        print(
            f"Error: Could not create render script '{render_script}': {e}",
            file=sys.stderr,
        )
        return False


def create_template_symlink(
    symlink_target: Path, template_path: Path, target_dir: Path
) -> bool:
    """Create a symlink to a template file.

    Args:
        symlink_target: Path where symlink should be created
        template_path: Path to template file to link to
        target_dir: Directory containing the symlink

    Returns:
        True if successful, False with warning message if symlink fails
    """
    try:
        rel_path = os.path.relpath(template_path, target_dir)
        symlink_target.symlink_to(rel_path)
        return True
    except OSError as e:
        # On Windows, symlinks may fail without admin/developer mode
        # Print warning but don't fail the command
        print(f"Warning: Could not create symlink: {e}", file=sys.stderr)
        print(
            f"You may need to manually copy or link to {template_path}", file=sys.stderr
        )
        return False


def create_quarto_project(
    dir_name: str,
    qmd_template_name: str,
    output_type: str,
    templates: dict[str, str],
) -> int:
    """Create a new Quarto project with specified templates.

    Args:
        dir_name: Directory name for the new project
        qmd_template_name: Name of the QMD template file
        output_type: Description of output type for success message
        templates: Dict mapping symlink names to template file names
                  e.g., {"simple-presentation.pptx": "simple-presentation.pptx"}

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    # Validate directory name
    if not validate_directory_name(dir_name):
        print(f"Error: Invalid directory name '{dir_name}'", file=sys.stderr)
        return 1

    # Get paths
    target_dir = Path(dir_name)
    base_name = target_dir.name
    qmd_file = target_dir / f"{base_name}.qmd"
    render_script = target_dir / "render.sh"

    # Get template paths
    template_qmd = get_template_path(qmd_template_name)
    template_render = get_template_path("render.sh.template")

    # Verify QMD and render templates exist
    if not verify_template_exists(template_qmd, "QMD template"):
        return 1
    if not verify_template_exists(template_render, "Render script template"):
        return 1

    # Verify all output templates exist
    template_paths: dict[str, Path] = {}
    for symlink_name, template_name in templates.items():
        template_path = get_template_path(template_name)
        if not verify_template_exists(template_path, f"Template {template_name}"):
            return 1
        template_paths[symlink_name] = template_path

    # Create directory
    if not create_directory(target_dir):
        return 1

    # Create QMD file from template
    if not create_qmd_file(qmd_file, template_qmd, base_name):
        return 1

    # Create render script from template
    if not create_render_script(render_script, template_render, base_name):
        return 1

    # Create symlinks to templates
    for symlink_name, template_path in template_paths.items():
        symlink_target = target_dir / symlink_name
        create_template_symlink(symlink_target, template_path, target_dir)

    # Success output
    print(f"Created: {qmd_file}")
    print(f"Output: {output_type}")
    print(f"Hint: Run 'cd {target_dir} && ./render.sh' to generate the output")

    return 0

