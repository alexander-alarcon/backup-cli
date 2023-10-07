from enum import StrEnum
from typing import NamedTuple

from .logger import ColoredLogger


class BackupStrategy(StrEnum):
    """
    Enum representing backup strategies.
    Currently, only supports 'incremental'.
    """

    INCREMENTAL = "incremental"


class BackupArgs(NamedTuple):
    """
    NamedTuple representing backup arguments.

    Attributes:
        source_directory (str): The source directory to be backed up.
        destination_directory (str): The destination directory to store the backup.
        logger (ColoredLogger): The logger to be used for logging.
    """

    source_directory: str
    destination_directory: str
    logger: ColoredLogger
