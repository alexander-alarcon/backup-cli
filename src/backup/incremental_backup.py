import os
import pathlib
import shutil

from src.logger import ColoredLogger, LogLevel

from .backup import Backup


class IncrementalBackup(Backup):
    def __init__(
        self, source_directory: str, destination_directory: str, logger: ColoredLogger
    ) -> None:
        """
        Initializes a new instance of the IncrementalBackup class, representing an
        incremental backup operation.

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
            link_target: str = os.readlink(source_file)
            try:
                # Check if the destination symlink already exists and points to a different target
                if (
                    destination_file_path.exists()
                    and os.readlink(destination_file_path) != link_target
                ):
                    os.remove(destination_file_path)  # Remove the existing symlink
                os.symlink(link_target, destination_file_path)
                self.logger.log(
                    LogLevel.COPY,
                    f"{source_file} (symlink) -> {destination_file_path}",
                )
            except FileExistsError:
                self.logger.log(
                    LogLevel.SKIP,
                    f"Symbolic link {source_file} already exists at destination.",
                )
        elif source_file.is_file():
            # If the source file is a regular file, copy it
            if not destination_file_path.exists() or (
                source_file.stat().st_size != destination_file_path.stat().st_size
                or source_file.stat().st_mtime != destination_file_path.stat().st_mtime
            ):
                shutil.copy2(source_file, destination_file_path)
                self.logger.log(
                    LogLevel.COPY, f"{source_file} -> {destination_file_path}"
                )
            else:
                self.logger.log(LogLevel.SKIP, f"File {source_file} is unchanged.")

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

    def perform_backup(self) -> None:
        """
        Performs an incremental backup by copying files from the source directory to the
        destination directory while skipping any files that have not been modified since
        the last backup.

        An incremental backup is a type of backup that only copies and updates files that
        have changed since the previous backup. This method ensures that only modified or
        new files are transferred to the destination directory, reducing the backup time
        and storage requirements compared to a full backup.

        Parameters:
            None.

        Returns:
            None.
        """
        self.__copy_files(
            source_directory=self.source_directory,
            destination_directory=self.destination_directory,
        )
