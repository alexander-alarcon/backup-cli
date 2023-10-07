import click

from src.backup.backup import Backup
from src.logger import ColoredLogger, LogLevel


@click.command()
@click.option(
    "-v", "--verbose", type=bool, is_flag=True, default=False, help="Verbose output."
)
@click.option(
    "-s",
    "--source",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
    help="Source directory to backup.",
)
@click.option(
    "-d",
    "--destination",
    type=click.Path(exists=False, dir_okay=True, file_okay=False),
    required=True,
    help="Destination directory to backup.",
)
def main(
    verbose: bool,
    source: str,
    destination: str,
) -> None:
    """Backup CLI."""
    logger = ColoredLogger(name="main", verbose=verbose)
    logger.log(LogLevel.INFO, "Starting backup.")

    backup = Backup(
        source_directory=source, destination_directory=destination, logger=logger
    )
    backup.perform_backup()

    logger.log(LogLevel.INFO, "Backup complete.")


if __name__ == "__main__":
    main()
