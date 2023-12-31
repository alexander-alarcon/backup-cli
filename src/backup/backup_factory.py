from src.type_definitions import BackupArgs, BackupStrategy

from .backup import Backup
from .full_backup import FullBackup
from .incremental_backup import IncrementalBackup
from .mirror_backup import MirrorBackup


class BackupFactory:
    @staticmethod
    def create_backup(
        backup_strategy: BackupStrategy, backup_args: BackupArgs
    ) -> Backup:
        """
        Create a backup based on the given backup strategy and arguments.

        Args:
            backup_strategy (BackupStrategy): The backup strategy to use.
            backup_args (BackupArgs): The arguments for the backup.

        Returns:
            Backup: The created backup instance.

        Raises:
            NotImplementedError: If the backup strategy is not implemented.

        """
        if backup_strategy == BackupStrategy.INCREMENTAL:
            return IncrementalBackup(
                source_directory=backup_args.source_directory,
                destination_directory=backup_args.destination_directory,
                logger=backup_args.logger,
            )
        if backup_strategy == BackupStrategy.FULL:
            return FullBackup(
                source_directory=backup_args.source_directory,
                destination_directory=backup_args.destination_directory,
                logger=backup_args.logger,
            )
        if backup_strategy == BackupStrategy.MIRROR:
            return MirrorBackup(
                source_directory=backup_args.source_directory,
                destination_directory=backup_args.destination_directory,
                logger=backup_args.logger,
            )
        else:
            raise NotImplementedError("Backup strategy not implemented.")
