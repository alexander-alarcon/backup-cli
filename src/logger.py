import logging
import sys
from enum import IntEnum, auto
from typing import Any

from colorama import Fore, Style, init

init(autoreset=True)


class LogLevel(IntEnum):
    """
    Enumeration of log levels.

    This enum defines log levels with associated integer values.
    """

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    SKIP = auto()
    COPY = auto()
    DELETE = auto()
    CUSTOM_LEVEL = auto()


class ColoredLogger:
    """
    A custom logger that adds colored formatting to log messages.

    Args:
        name (str): The name of the logger.
        verbose (bool, optional): Whether to enable verbose logging. Defaults to False.

    Attributes:
        COLORS (dict[LogLevel, str]): A mapping of log levels to color codes.
    """

    COLORS: dict[LogLevel, str] = {
        LogLevel.DEBUG: Fore.CYAN,
        LogLevel.INFO: Fore.BLUE,
        LogLevel.WARNING: Fore.YELLOW,
        LogLevel.ERROR: Fore.RED,
        LogLevel.CRITICAL: f"{Fore.RED}{Style.BRIGHT}",
        LogLevel.SKIP: Fore.YELLOW,
        LogLevel.COPY: Fore.CYAN,
        LogLevel.DELETE: Fore.MAGENTA,
    }

    def __init__(self, name: str, verbose: bool = False) -> None:
        """
        Initialize the ColoredLogger.

        Args:
            name (str): The name of the logger.
            verbose (bool, optional): Whether to enable verbose logging. Defaults to False.
        """
        self.logger: logging.Logger = logging.getLogger(name)

        if not self.logger.handlers:
            self.logger.propagate = False  # Disable logger propagation

        log_format = "%(message)s"
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(self.ColoredFormatter(log_format))
        self.logger.addHandler(console_handler)

        logging.basicConfig(
            level=LogLevel.DEBUG if verbose else logging.CRITICAL,
            handlers=[
                console_handler,
            ],
        )

    class ColoredFormatter(logging.Formatter):
        """
        A custom log formatter that adds color and log level to log messages.

        Args:
            fmt (str): The log message format.
        """

        LEVEL_NAMES: dict[LogLevel, str] = {
            LogLevel.DEBUG: "DEBUG",
            LogLevel.INFO: "INFO",
            LogLevel.WARNING: "WARNING",
            LogLevel.ERROR: "ERROR",
            LogLevel.CRITICAL: "CRITICAL",
            LogLevel.SKIP: "SKIP",
            LogLevel.COPY: "COPY",
            LogLevel.DELETE: "DELETE",
        }

        def __init__(self, fmt: str) -> None:
            """
            Initialize the ColoredFormatter.

            Args:
                fmt (str): The log message format.
            """
            super().__init__(fmt)

        def format(self, record: logging.LogRecord) -> str:
            """
            Format a log record with color and log level.

            Args:
                record (logging.LogRecord): The log record to format.

            Returns:
                str: The formatted log message.
            """
            log_level = LogLevel(record.levelno)

            level_name: str = self.LEVEL_NAMES.get(log_level, record.levelname)

            log_level_color: str = ColoredLogger.COLORS.get(log_level, "")
            log_message: str = super().format(record)
            return f"{log_level_color}[{level_name}]:{Style.RESET_ALL} {log_message}"

    def log(self, level: LogLevel, message: str, *args: Any, **kwargs: Any) -> None:
        """
        Log a message with the specified log level.

        Args:
            level (LogLevel): The log level to use.
            message (str): The log message.
            *args (Any): Additional positional arguments for the log message.
            **kwargs (Any): Additional keyword arguments for the log message.

        Raises:
            ValueError: If the specified log level is not defined in the LogLevel enum.
        """
        if level in LogLevel.__members__.values():
            level_value: int = level.value

            self.logger.log(level_value, message, *args, **kwargs)
        else:
            raise ValueError(f"Custom log level '{level}' is not defined.")
