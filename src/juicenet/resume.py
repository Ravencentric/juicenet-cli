import csv
from pathlib import Path

from loguru import logger

from .files import get_file_info


class Resume:
    """
    A class representing a resume manager for logging and checking already uploaded files

    Attributes:
        - `path (Path)`: The path to the resume file
        - `disable (bool)`: A flag to enable or disable this class

    Methods:
        - `log_file_info(self, file: Path) -> None`: Logs file information to the resume file if logging is enabled
        - `filter_uploaded_files(self, files: list[Path]) -> list[Path]`: Filters out already uploaded files from
            the provided list based on resume data

    This class is used to manage resume information, including logging file details and checking for already uploaded files
    """

    def __init__(self, path: Path, scope: str, disable: bool = False) -> None:
        self.path = path
        self.scope = scope
        self.disable = disable

    def log_file_info(self, file: Path) -> None:
        """
        Logs file information to the resume file if logging is enabled
        """
        if not self.disable:
            info = get_file_info(file)
            info["scope"] = self.scope
            csv.DictWriter(
                self.path.open("a"), fieldnames=["name", "size", "count", "scope"], quoting=csv.QUOTE_ALL
            ).writerow(info)
            logger.debug(f"Writing file information to resume: {file}")

    def filter_uploaded_files(self, files: list[Path]) -> list[Path]:
        """
        Filters out already uploaded files from the given list based on resume data
        """
        if not self.disable:
            not_uploaded = []
            resume_data = tuple(
                csv.DictReader(
                    self.path.open("r"), fieldnames=["name", "size", "count", "scope"], quoting=csv.QUOTE_ALL
                )
            )

            for file in files:
                info = get_file_info(file)
                info["scope"] = self.scope
                if info in resume_data:
                    logger.info(f"Skipping: {file.name} - Already uploaded")
                else:
                    not_uploaded.append(file)

            return not_uploaded

        else:
            return files

    def clear_resume(self) -> None:
        """
        Clear resume data
        """
        self.path.unlink(missing_ok=True)
        logger.info(f"Cleared {self.path}")
