import pathlib
from abc import ABC, abstractmethod

from src.logger import ColoredLogger


class Backup(ABC):
    def __init__(
        self, source_directory: str, destination_directory: str, logger: ColoredLogger
    ) -> None:
        """
        Initializes a new instance of the Backup class, which serves as an abstract base
        class for various backup operations. This class defines the common attributes and
        behavior shared by different types of backups.

        Args:
            source_directory (str): The source directory containing data to be backed up.
            destination_directory (str): The destination directory where the backup data
                will be stored.
            logger (ColoredLogger): The logger instance used for recording backup
                progress and any related messages.

        Attributes:
            source_directory (pathlib.Path): A pathlib.Path object representing the path to
                the source directory.
            destination_directory (pathlib.Path): A pathlib.Path object representing the
                path to the destination directory.
            logger (ColoredLogger): The logger instance used for logging backup operations.

        Raises:
            NotImplementedError: This class is intended to be subclassed, so attempting
                to create an instance of this abstract base class will raise an error.

        """
        self.source_directory = pathlib.Path(source_directory)
        self.destination_directory = pathlib.Path(destination_directory)
        self.logger: ColoredLogger = logger

    @abstractmethod
    def perform_backup(self) -> None:
        """
        Perform a backup operation.

        This method should be implemented in subclasses to define the specific logic
        and steps required to perform a backup. Subclasses should override this method
        to provide backup functionality tailored to their particular use case.

        Raises:
            NotImplementedError: Subclasses must implement this method to define the
                backup procedure.

        """
        raise NotImplementedError("perform_backup must be implemented.")
