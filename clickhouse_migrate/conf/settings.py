import configparser
import json
from os import path

from typing import Optional, Tuple, List


from envparse import env

from clickhouse_migrate.common.exceptions.config import ConfigError
from clickhouse_migrate.common.meta import Singleton

env.read_envfile()

CLICKHOUSE_MIGRATE_DATABASES = env.str("CLICKHOUSE_MIGRATE_DATABASES", default=None)
CLICKHOUSE_MIGRATE_DIRECTORY = env.str("CLICKHOUSE_MIGRATE_DIRECTORY", default=None)


class Settings(metaclass=Singleton):
    CONFIG_PATH = path.join("./clickhouse_migrate.ini")
    DEFAULT_MIGRATIONS_DIR = path.join("./migrations")

    databases = (
        json.loads(CLICKHOUSE_MIGRATE_DATABASES)
        if CLICKHOUSE_MIGRATE_DATABASES
        else None
    )
    migration_dir = CLICKHOUSE_MIGRATE_DIRECTORY

    def init_config(
        self,
        config_path: Optional[str] = CONFIG_PATH,
        databases: Optional[str] = None,
        migration_dir: Optional[str] = DEFAULT_MIGRATIONS_DIR,
    ):
        if self.databases is None:

            if not databases:
                databases, migration_dir = self.__get_params_from_config_file(
                    config_path=config_path
                )

            self.databases = databases
            self.migration_dir = migration_dir

        self.__post_init_checks()

    @staticmethod
    def __get_params_from_config_file(config_path: str) -> Tuple[str, List[str]]:
        try:
            config = configparser.ConfigParser()
            config.read(config_path)

            return json.loads(
                config.get("databases", "connection_strings")
            ), json.loads(config.get("migration_path", "directory"))
        except KeyError:
            raise ConfigError(
                "Variables: connection_strings, directory must be provided in the *.ini config file"
            )

    def __post_init_checks(self):
        if self.databases is None:
            raise ConfigError(
                "Unable to configure migration tool. None of the configuration options were provided"
            )
        if not path.isdir(self.migration_dir):
            raise ConfigError(
                "Unable to configure migration tool. Provided migration dir does not exist"
            )


if __name__ == "__main__":
    settings = Settings()
    settings.init_config(config_path="./tests/clickhouse_migrate_test.ini")
