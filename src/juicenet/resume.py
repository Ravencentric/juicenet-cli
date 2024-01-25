import csv
from pathlib import Path
from typing import Any, Union

from loguru import logger

from .utils import get_file_info


class Resume:
    """
    A class representing a resume manager.

    Attributes:
        - `path (Path)`: The path to the resume file.
        - `scope (str)`: The scope of the nzbs made by Nyuu (Private or Public). Useful as additional metadata.
        - `disable (bool)`: A flag to enable or disable this class.

    Methods:
        - `log_file_info(self, file: Path) -> None`: Logs file information to the resume file if logging is enabled.
        - `filter_uploaded_files(self, files: list[Path]) -> list[Path]`: Filters out already uploaded files from
            the provided list based on resume data.

    This class is used to manage resume information, including logging file details and checking for already uploaded files.
    """

    def __init__(self, path: Path, scope: str, disable: bool = False) -> None:
        self.path = path
        self.scope = scope
        self.disable = disable

    def write_resume(self, info: dict[str, str]) -> None:
        """
        This method takes a dictionary containing information
        about a file or folder and writes it into a CSV file.
        The dictionary should contain the following keys:

        ```py
        info = {
            "name": "filename.mkv",
            "size": "123456789", # in bytes
            "count": "1", # number of files if it's a folder, 1 if it's a single file
            "scope": "private" # or public
        }
        ```
        """
        csv.DictWriter(
            self.path.open("a", encoding="utf-8"),
            fieldnames=["name", "size", "count", "scope"],
            quoting=csv.QUOTE_ALL,
        ).writerow(info)

    def read_resume(self) -> tuple[dict[Union[str, Any], Union[str, Any]], ...]:
        """
        Reads the resume data from a CSV file written by `Resume.write_resume()`

        Returns a tuple of dictionaries like:

        ```py
        data = (
            {"name": "filename.mkv", "size": "123456789", "count": "1", "scope": "private"},
            {"name": "foldername", "size": "987654321", "count": "3", "scope": "public"}
        )
        ```

        """
        data = tuple(
            csv.DictReader(
                self.path.open("r", encoding="utf-8"),
                fieldnames=["name", "size", "count", "scope"],
                quoting=csv.QUOTE_ALL,
            )
        )
        return data

    def log_file_info(self, file: Path) -> None:
        """
        Logs file information to the resume file if logging is enabled
        """
        if not self.disable:
            info = get_file_info(file)
            info["scope"] = self.scope
            self.write_resume(info)
            logger.debug(f"Saving to resume: {info}")

    def already_uploaded(self, file: Path) -> bool:
        """
        Check if a given file is already uploaded by juicenet
        """
        if not self.disable:
            resume_data = self.read_resume()

            info = get_file_info(file)
            info["scope"] = self.scope

            if info in resume_data:
                return True

            return False

        return False

    def filter_uploaded_files(self, files: list[Path]) -> list[Path]:
        """
        Filters out already uploaded files from the given list based on resume data
        """
        if not self.disable:
            not_uploaded = []
            resume_data = self.read_resume()

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
