import os
from pathlib import Path
from typing import Any, Generator


class DirectoryTree:
    def __init__(self, root_dir: str) -> None:
        """
        Initializes a new instance of the class with the specified root directory.

        Parameters:
            root_dir (str): The root directory for the instance.

        Raises:
            ValueError: If the specified directory does not exist.
        """
        self.root_dir: str = root_dir

        if not Path(self.root_dir).is_dir():
            raise ValueError(
                f"The specified directory '{self.root_dir}' does not exist."
            )

    def count_items(self) -> dict[str, int]:
        """
        Counts the number of items in the directory.

        Returns:
            A dictionary containing the following counts:
                - "Total files": The total number of files in the directory.
                - "Total symlinks": The total number of symbolic links in the directory.
                - "Total directories": The total number of directories in the directory, including the root directory.

        """
        total_files: int = len(list(self._find_files()))
        total_symlinks: int = len(list(self._find_symlinks()))
        total_directories: int = (
            len(list(self._find_directories())) + 1
        )  # Include the root directory

        return {
            "Total files": total_files,
            "Total symlinks": total_symlinks,
            "Total directories": total_directories,
        }

    def _find_files(self) -> Generator[str, Any, None]:
        """
        Generates a list of file paths by recursively traversing the directory tree starting from the root directory.

        Returns:
            A generator that yields file paths as strings.
        """
        for dirpath, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_path: str = os.path.join(dirpath, filename)
                if not os.path.islink(file_path):  # Exclude symlinks
                    yield file_path

    def _find_symlinks(self) -> Generator[str, Any, None]:
        """
        Find symlinks in the directory tree rooted at `root_dir`.

        :return: A generator object that yields the paths of all symlinks found.
        :rtype: generator
        """
        for dirpath, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_path: str = os.path.join(dirpath, filename)
                if os.path.islink(file_path):
                    yield file_path

    def _find_directories(self) -> Generator[str, Any, None]:
        """
        Iterates over all directories in the given root directory and yields the path of each directory.

        :return: A generator that yields the path of each directory.
        """
        for dirpath, dirnames, _ in os.walk(self.root_dir):
            for dirname in dirnames:
                yield os.path.join(dirpath, dirname)


# Usage example:
if __name__ == "__main__":
    root_directory = "dummy_tree"
    tree = DirectoryTree(root_directory)

    counts = tree.count_items()
    for item, count in counts.items():
        print(f"{item}: {count}")
