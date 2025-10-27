"""PDF export command for Word documents."""

from pathlib import Path

from quarto4sbp.utils.pdf_export import (
    export_to_pdf_via_applescript,
    find_stale_files,
    process_files,
    validate_directory,
)


def export_docx_to_pdf(docx_path: Path) -> bool:
    """Export a DOCX file to PDF using Word via AppleScript.

    Exports directly in the current directory where the DOCX file is located.

    Args:
        docx_path: Path to DOCX file to export

    Returns:
        True if export succeeded, False otherwise
    """
    # Calculate PDF path using double extension
    pdf_path = Path(str(docx_path) + ".pdf")

    # Build AppleScript to export PDF
    applescript = f"""
tell application "Microsoft Word"
    open POSIX file "{docx_path.resolve()}"
    set theDoc to active document
    save as theDoc file name POSIX file "{pdf_path.resolve()}" file format format PDF
    close theDoc saving no
end tell
"""

    return export_to_pdf_via_applescript(docx_path, applescript, "Word")


def cmd_pdf_docx(args: list[str]) -> int:
    """Handle the pdf-docx subcommand.

    Args:
        args: Optional directory argument (defaults to current directory)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Determine target directory
    directory = validate_directory(args)
    if directory is None:
        return 1

    # Find stale DOCX files
    stale_docx = find_stale_files(directory, "docx")

    # Process files
    return process_files(stale_docx, export_docx_to_pdf, "DOCX")
