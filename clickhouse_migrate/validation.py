from os import path

from clickhouse_migrate.common.exceptions.config import ConfigError
from clickhouse_migrate.conf.settings import Settings


def check_migrations_dir():
    if not path.isdir(Settings().migration_dir):
        raise ConfigError(f"Provided migration directory {Settings().migration_dir} does not exist")


def check_databases():
    if Settings().databases is None:
        raise ConfigError("Databases were not provided")
