import os
import random
import string
from typing import LiteralString


class RandomTreeGenerator:
    def __init__(self, root_dir: str, max_depth: int, max_files_per_dir: int) -> None:
        self.root_dir: str = root_dir
        self.max_depth: int = max_depth
        self.max_files_per_dir: int = max_files_per_dir

    def generate_random_string(self, length: int) -> str:
        letters: LiteralString = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))

    def generate_random_tree(self) -> None:
        if self.max_depth <= 0:
            return

        os.makedirs(self.root_dir, exist_ok=True)

        num_files: int = random.randint(1, self.max_files_per_dir)
        for _ in range(num_files):
            file_name: str = self.generate_random_string(10) + ".txt"
            file_path: str = os.path.join(self.root_dir, file_name)
            with open(file_path, "w") as file:
                file.write("This is a random text file.")

        num_subdirs: int = random.randint(1, 2)  # Random number of subdirectories
        for _ in range(num_subdirs):
            subdir_name: str = self.generate_random_string(5)
            subdir_path: str = os.path.join(self.root_dir, subdir_name)
            RandomTreeGenerator(
                subdir_path, self.max_depth - 1, self.max_files_per_dir
            ).generate_random_tree()

        if num_files > 0 and random.random() < 0.5:
            link_name: str = self.generate_random_string(5) + ".link"
            link_path: str = os.path.join(self.root_dir, link_name)

            files_in_directory: list[str] = [
                f
                for f in os.listdir(self.root_dir)
                if os.path.isfile(os.path.join(self.root_dir, f))
            ]

            if files_in_directory:
                link_target: str = os.path.relpath(
                    os.path.join(self.root_dir, random.choice(files_in_directory)),
                    self.root_dir,
                )
                os.symlink(link_target, link_path)
