import filecmp
import pytest
from pathlib import Path
from src.dialog2rasa.cli import main


@pytest.fixture
def mock_args(monkeypatch):
    """Set up command line arguments for the tool with a temporary output directory."""
    input_dir = Path("tests/mockup-agent")
    monkeypatch.setattr("sys.argv", ["dialog2rasa", "--path", str(input_dir)])
    return input_dir


def compare_file_contents_detailed(file1, file2):
    """Compare the contents of two files, returning detailed discrepancies."""
    discrepancies = []
    with open(file1, "r") as f1, open(file2, "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    for i, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
        if line1 != line2:
            discrepancies.append(
                f"Mismatch in line {i}: '{line1.strip()}' vs '{line2.strip()}'"
            )

    # Check for extra lines in either file
    if len(lines1) > len(lines2):
        discrepancies.append(
            f"Extra lines in {file1} starting from line {len(lines2)+1}"
        )
    elif len(lines2) > len(lines1):
        discrepancies.append(
            f"Extra lines in {file2} starting from line {len(lines1)+1}"
        )

    return discrepancies


def compare_directories(dir1, dir2):
    """Integrate detailed file content comparison into the directory comparison logic."""
    discrepancies = []
    comparison = filecmp.dircmp(dir1, dir2)

    # Handle file/directory existence discrepancies
    if comparison.left_only:
        discrepancies.append(
            f"Extra files/directories in {dir1}: {comparison.left_only}"
        )
    if comparison.right_only:
        discrepancies.append(
            f"Missing files/directories in {dir1}, found in {dir2}: {comparison.right_only}"
        )

    # Detailed content comparison for mismatched files
    for filename in comparison.diff_files:
        file1, file2 = Path(dir1) / filename, Path(dir2) / filename
        file_discrepancies = compare_file_contents_detailed(file1, file2)
        if file_discrepancies:
            discrepancies.append(f"Discrepancies in {filename}:")
            discrepancies.extend(file_discrepancies)

    # Recursively compare common subdirectories
    for common_dir in comparison.common_dirs:
        sub_discrepancies = compare_directories(
            Path(dir1) / common_dir, Path(dir2) / common_dir
        )
        discrepancies.extend(sub_discrepancies)

    return discrepancies


def test_conversion(mock_args):
    input_dir = mock_args

    main()  # Executes the conversion process

    output_dir = input_dir / "output"
    reference_output_dir = input_dir / "reference_output"

    discrepancies = compare_directories(output_dir, reference_output_dir)
    assert not discrepancies, "Detailed discrepancies found:\n" + "\n".join(
        discrepancies
    )
