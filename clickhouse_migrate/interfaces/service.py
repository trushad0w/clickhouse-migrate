import glob
import importlib.util
import logging
import re
from datetime import datetime, timezone
from hashlib import md5
from pathlib import Path
from typing import List

from clickhouse_migrate.conf.settings import Settings
from clickhouse_migrate.interfaces.repo import MigrationRepo
from clickhouse_migrate.models.migration import Step, MigrationMeta

logger = logging.getLogger(__name__)


class MigrationService:
    MIGRATIONS_VARIABLE = "migrations"
    MIGRATION_TEMPLATE = f"""
from clickhouse_migrate import Step

{MIGRATIONS_VARIABLE} = [Step(sql="")]
"""
    DATETIME_FORMAT = "%Y-%m-%d-%H-%M-%S"

    def __init__(self):
        self.datetime_re = re.compile(
            rf"{Settings().migration_dir}/([0-9]{{4}}(-[0-9]{{2}}){{5}})_.*"
        )
        migration_meta_list = MigrationRepo.get_applied_migrations()
        self.applied_migration_map = {
            meta.migration_id: meta.migration_hash for meta in migration_meta_list
        }

    @staticmethod
    def apply_initial_step():
        MigrationRepo.init_migration_table()

    @classmethod
    def create_new_migration(cls, name: str):
        """
        Create blank migration with the provided name and current timestamp
        :param name:
        :return:
        """
        file_name = f"{Settings().migration_dir}/{datetime.now(tz=timezone.utc).strftime(cls.DATETIME_FORMAT)}_{name}.py"
        with open(file_name, "w") as f:
            f.write(cls.MIGRATION_TEMPLATE)
        logging.info(f"Migration: {file_name} has been created")

    def apply_all_migrations(self):
        migration_path_list = self.get_migration_list()
        for file_path in migration_path_list:
            self.__apply_migrations_for_db(file_path)

    def get_migration_list(self) -> List[str]:
        """
        Get migration files from directory
        :return: List of migration files paths
        """
        file_list = [
            file
            for file in glob.glob(f"{Settings().migration_dir}/*.py")
            if self.datetime_re.match(file)
        ]
        file_list.sort(
            key=lambda x: datetime.strptime(
                self.datetime_re.match(x).groups()[0], self.DATETIME_FORMAT
            )
        )
        return file_list

    def __apply_migrations_for_db(self, file_path: str):
        """
        Importing migration contents here to access steps that are defined in a selected migration file
        and apply each step by executing sql statement defined in it
        :param file_path: path to a migration
        """
        spec = importlib.util.spec_from_file_location(
            self.MIGRATIONS_VARIABLE, file_path
        )
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)

        migration_list: List[Step] = migration_module.__getattribute__(
            self.MIGRATIONS_VARIABLE
        )
        for idx, migration in enumerate(migration_list):
            filename = self.get_filename(file_path=file_path)
            migration_meta = MigrationMeta(
                migration_id=f"{filename}_{idx}",
                migration_hash=md5(
                    re.sub(r"\s+", "", migration.sql).encode("utf8")
                ).hexdigest(),
                filename=filename,
            )
            if self.is_applied_migration(migration_meta):
                continue
            logger.info(f"Applying migration - {migration_meta.migration_id}")
            MigrationRepo.apply_migration(step=migration, migration_meta=migration_meta)

    def is_applied_migration(self, migration_meta: MigrationMeta) -> bool:
        if self.applied_migration_map.get(migration_meta.migration_id):
            if (
                self.applied_migration_map[migration_meta.migration_id]
                != migration_meta.migration_hash
            ):
                raise ValueError(
                    f"Migration content changed in the already applied file: {migration_meta.filename}"
                )
            return True
        return False

    @staticmethod
    def get_filename(file_path: str) -> str:
        path = Path(file_path)
        path.with_suffix("")
        return path.stem
