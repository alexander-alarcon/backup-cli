import os
import pathlib
import shutil

from src.logger import ColoredLogger, LogLevel

from .backup import Backup


class MirrorBackup(Backup):
    def __init__(
        self, source_directory: str, destination_directory: str, logger: ColoredLogger
    ) -> None:
        """
        Initializes a new instance of the MirrorBackup class, representing a full backup operation.

        Args:
            source_directory (str): The source directory from which data will be backed up.
            destination_directory (str): The destination directory where the backup data
                will be stored.
            logger (ColoredLogger): The logger instance used for recording backup
                progress, errors, and any related messages.

        Returns:
            None
        """
        super().__init__(
            source_directory=source_directory,
            destination_directory=destination_directory,
            logger=logger,
        )

    def __create_directory(self, directory: pathlib.Path) -> None:
        """
        Create a directory.

        Args:
            directory (pathlib.Path): The path of the directory to be created.

        Returns:
            None

        Raises:
            OSError: If the creation of the directory fails.

        """
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError:
            self.logger.log(
                LogLevel.ERROR, f"Creation of the directory {directory} failed"
            )

    def __copy_file(
        self, source_file: pathlib.Path, destination_file_path: pathlib.Path
    ) -> None:
        """
        Copies a file from the source path to the destination path.

        Args:
            source_file (pathlib.Path): The path to the source file.
            destination_file_path (pathlib.Path): The path to the destination file.

        Returns:
            None
        """
        if not source_file.exists():
            self.logger.log(
                LogLevel.ERROR, f"[ERROR] Source file {source_file} does not exist."
            )
            return

        if source_file.is_symlink():
            self.logger.log(LogLevel.INFO, f"{source_file} is a symlink")
            link_target: str = os.readlink(source_file)
            # Remove the existing symlink if it exists
            if destination_file_path.exists():
                os.remove(destination_file_path)

            os.symlink(link_target, destination_file_path)
            self.logger.log(
                LogLevel.COPY,
                f"{source_file} (symlink) -> {destination_file_path}",
            )
        elif source_file.is_file():
            # If the source file is a regular file, copy it
            shutil.copy2(source_file, destination_file_path)
            self.logger.log(LogLevel.COPY, f"{source_file} -> {destination_file_path}")

    def __copy_files(
        self, source_directory: pathlib.Path, destination_directory: pathlib.Path
    ) -> None:
        """
        Copy files from the source directory to the destination directory recursively.

        Parameters:
            source_directory (pathlib.Path): The path to the source directory.
            destination_directory (pathlib.Path): The path to the destination directory.

        Returns:
            None: This function does not return anything.
        """
        self.logger.log(
            LogLevel.INFO,
            f"Copying from: {self.source_directory} -> to: {self.destination_directory}",
        )

        source_dir_path: pathlib.Path = source_directory
        destination_dir_path: pathlib.Path = destination_directory

        self.__create_directory(destination_dir_path)

        for source_file in source_dir_path.iterdir():
            destination_file_path: pathlib.Path = (
                destination_dir_path / source_file.name
            )

            self.__copy_file(
                source_file=source_file,
                destination_file_path=destination_file_path,
            )

            if source_file.is_dir():
                subdirectory: pathlib.Path = source_dir_path / source_file.name
                self.__copy_files(
                    source_directory=subdirectory,
                    destination_directory=destination_file_path,
                )

    def __delete_extra_files(
        self, source_directory: pathlib.Path, destination_directory: pathlib.Path
    ) -> None:
        """
        Recursively delete extra files in the destination directory that are not in the source directory.

        Args:
            source_directory (pathlib.Path): The path to the source directory.
            destination_directory (pathlib.Path): The path to the destination directory.

        Returns:
            None
        """
        for item in destination_directory.iterdir():
            item_in_source: pathlib.Path = source_directory / item.name

            if item.is_file() and not item_in_source.exists():
                self.logger.log(LogLevel.DELETE, f"Deleting {item}")
                os.remove(item)

            # If the item is a directory, call this method recursively
            elif item.is_dir():
                self.__delete_extra_files(
                    source_directory=item_in_source, destination_directory=item
                )

    def perform_backup(self) -> None:
        """
        Perform a mirror backup operation.

        This method copies files from the source directory to the destination directory,
        overwriting existing files if conflicts occur. Symbolic links are updated to
        point to the same targets as in the source directory. Extra files in the
        destination directory that are not present in the source directory will be deleted.

        Warning: This operation may delete files in the destination directory to mirror
        the source. Use with caution to avoid unintentional data loss.

        Returns:
            None
        """
        self.__copy_files(
            source_directory=self.source_directory,
            destination_directory=self.destination_directory,
        )
        self.__delete_extra_files(
            source_directory=self.source_directory,
            destination_directory=self.destination_directory,
        )
