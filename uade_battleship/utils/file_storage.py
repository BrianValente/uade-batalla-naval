import os
from typing import Optional


class FileStorage:
    PREFIX = "storage/"

    @staticmethod
    def read_file(path: str) -> Optional[str]:
        """
        Reads a file and returns its content.

        Args:
            path (str): The relative path to the file.
        """

        path = f"{FileStorage.PREFIX}{path}"

        try:
            with open(path, "r") as file:
                return file.read()
        except Exception:
            return None

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """
        Writes content to a file.

        Args:
            path (str): The relative path to the file.
            content (str): The content to write.
        """

        # Create the storage directory if it doesn't exist
        if not os.path.exists(FileStorage.PREFIX):
            os.makedirs(FileStorage.PREFIX)

        path = f"{FileStorage.PREFIX}{path}"

        with open(path, "w") as file:
            file.write(content)

    @staticmethod
    def delete_file(path: str) -> None:
        """
        Deletes a file.
        """
        path = f"{FileStorage.PREFIX}{path}"
        os.remove(path)
