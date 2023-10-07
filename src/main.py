from typing import Optional

import click

from .backup.backup import Backup
from .backup.backup_factory import BackupFactory
from .logger import ColoredLogger, LogLevel
from .type_definitions import BackupArgs, BackupStrategy


def validate_backup_strategy(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> BackupStrategy:
    """
    Validate the provided backup strategy.

    Args:
        ctx (click.Context): The click context object.
        param (click.Parameter): The click parameter object.
        value (Optional[str]): The value of the backup strategy.

    Returns:
        BackupStrategy: The validated backup strategy.

    Raises:
        click.BadParameter: If the backup strategy is invalid.
    """
    if value is None:
        return BackupStrategy.INCREMENTAL
    try:
        return BackupStrategy(value)
    except ValueError:
        raise click.BadParameter(
            f"Invalid backup strategy '{value}'. Please use 'incremental' or 'full'."
        )


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
@click.option(
    "-bs",
    "--backup-strategy",
    type=click.Choice(
        [strategy.value for strategy in BackupStrategy], case_sensitive=False
    ),
    callback=validate_backup_strategy,
    help="Choose a backup strategy: incremental, etc.",
    show_default=True,
    show_choices=True,
    default=BackupStrategy.INCREMENTAL.value,
)
def main(
    verbose: bool, source: str, destination: str, backup_strategy: BackupStrategy
) -> None:
    """Backup CLI."""
    logger = ColoredLogger(name="main", verbose=verbose)
    logger.log(LogLevel.INFO, "Starting backup.")

    backup: Backup = BackupFactory.create_backup(
        backup_strategy=backup_strategy,
        backup_args=BackupArgs(
            source_directory=source,
            destination_directory=destination,
            logger=logger,
        ),
    )
    backup.perform_backup()

    logger.log(LogLevel.INFO, "Backup complete.")


if __name__ == "__main__":
    main()
