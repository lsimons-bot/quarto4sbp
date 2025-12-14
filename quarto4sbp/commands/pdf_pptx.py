"""PDF export command for PowerPoint files."""

from pathlib import Path

from quarto4sbp.utils.pdf_export import (
    export_to_pdf_via_applescript,
    find_stale_files,
    process_files,
    validate_directory,
)


def export_pptx_to_pdf(pptx_path: Path) -> bool:
    """Export a PPTX file to PDF using PowerPoint via AppleScript.

    Exports directly in the current directory where the PPTX file is located.

    Args:
        pptx_path: Path to PPTX file to export

    Returns:
        True if export succeeded, False otherwise
    """
    # Calculate PDF path using double extension
    pdf_path = Path(str(pptx_path) + ".pdf")

    # Build AppleScript to export PDF
    applescript = f"""
tell application "Microsoft PowerPoint"
    open POSIX file "{pptx_path.resolve()}"
    set theDoc to active presentation
    save theDoc in POSIX file "{pdf_path.resolve()}" as save as PDF
    close theDoc
end tell
"""

    return export_to_pdf_via_applescript(pptx_path, applescript, "PowerPoint")


def cmd_pdf_pptx(args: list[str]) -> int:
    """Handle the pdf-pptx subcommand.

    Args:
        args: Optional directory argument (defaults to current directory)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Determine target directory
    directory = validate_directory(args)
    if directory is None:
        return 1

    # Find stale PPTX files
    stale_pptx = find_stale_files(directory, "pptx")

    # Process files
    return process_files(stale_pptx, export_pptx_to_pdf, "PPTX")
