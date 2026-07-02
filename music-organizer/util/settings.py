"""
settings.py

Class that tracks filepaths and folderpaths for temporary and results folders.
"""

from pathlib import Path


class Settings:
    """
    Class for tracking path for temporary and results folders.
    """

    def __init__(self, temp_dir_in: Path, results_dir_in: Path, complete_dir_in: Path) -> None:
        # For holding extracted folders
        self.temp_dir: Path = temp_dir_in
        self.temp_dir.mkdir(exist_ok=True)

        # Holding the final, flattened, organized folders
        self.results_dir: Path = results_dir_in
        self.results_dir.mkdir(exist_ok=True)

        # Holding archived files that have been successfully extracted and flattened/organized
        self.complete_dir: Path = complete_dir_in
        self.complete_dir.mkdir(exist_ok=True)
