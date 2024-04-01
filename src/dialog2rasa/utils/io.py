import json
import shutil
from pathlib import Path


def reset_directory(dir_path: Path, deepest_subdir: str) -> None:
    """
    Deletes all files and folders in the specified directory recursively,
    then creates the specified deepest subdirectory.
    """
    if dir_path.exists():
        shutil.rmtree(dir_path)
    (dir_path / deepest_subdir).mkdir(parents=True, exist_ok=True)


def read_json_file(file_path: Path) -> dict:
    """Reads and returns JSON data from a file."""
    with Path(file_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def write_to_file(file_path: Path, content: str, mode: str = "w") -> None:
    """Writes given content to a file."""
    with Path(file_path).open(mode, encoding="utf-8") as file:
        file.write(content)


def write_dict_files(content_dict: dict) -> None:
    """Writes given content to corresponding files."""
    for file_path, content in content_dict.items():
        write_to_file(file_path, content, mode="a")
