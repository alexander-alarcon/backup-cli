import os
import random
import string
from typing import LiteralString

import click

from src.logger import ColoredLogger, LogLevel


def generate_random_string(length: int) -> str:
    """Generate a random string of given length."""
    letters: LiteralString = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_random_tree(root_dir: str, max_depth: int, max_files_per_dir: int) -> None:
    """Generate a random directory tree with files and symbolic links."""

    if max_depth <= 0:
        return

    os.makedirs(root_dir, exist_ok=True)

    num_files: int = random.randint(1, max_files_per_dir)
    for _ in range(num_files):
        file_name: str = generate_random_string(10) + ".txt"
        file_path: str = os.path.join(root_dir, file_name)
        with open(file_path, "w") as file:
            file.write("This is a random text file.")

    num_subdirs: int = random.randint(1, 2)  # Random number of subdirectories
    for _ in range(num_subdirs):
        subdir_name: str = generate_random_string(5)
        subdir_path: str = os.path.join(root_dir, subdir_name)
        generate_random_tree(subdir_path, max_depth - 1, max_files_per_dir)

    if num_files > 0 and random.random() < 0.5:
        link_name: str = generate_random_string(5) + ".link"
        link_path: str = os.path.join(root_dir, link_name)

        # Get a list of files in the directory
        files_in_directory: list[str] = [
            f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))
        ]

        if files_in_directory:
            link_target: str = os.path.relpath(
                os.path.join(root_dir, random.choice(files_in_directory)), root_dir
            )
            os.symlink(link_target, link_path)


@click.command()
@click.argument("root_directory", type=str)
@click.option(
    "-d", "--max-depth", type=int, default=4, help="Maximum depth of the tree"
)
@click.option(
    "-f",
    "--max-files-per-dir",
    type=int,
    default=5,
    help="Maximum number of files per directory",
)
def main(root_directory: str, max_depth: int, max_files_per_dir: int) -> None:
    """
    Generate a random directory tree.

    Parameters:
        root_directory (str): Name of the root directory for the tree
        max_depth (int): Maximum depth of the tree (default: 4)
        max_files_per_dir (int): Maximum number of files per directory (default: 5)

    Returns:
        None
    """
    logger = ColoredLogger(name="main", verbose=True)

    generate_random_tree(
        root_dir=root_directory,
        max_depth=max_depth,
        max_files_per_dir=max_files_per_dir,
    )
    logger.log(LogLevel.INFO, f"Random tree generated in {root_directory}")


if __name__ == "__main__":
    main()
