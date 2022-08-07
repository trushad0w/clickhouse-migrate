from os import path
from typing import List, Optional

from envparse import env

from clickhouse_migrate.common.meta import Singleton

env.read_envfile()


class Settings(metaclass=Singleton):
    DATABASES_ENV_VAR = "CLICKHOUSE_MIGRATE_DATABASES"
    DIRECTORY_ENV_VAR = "CLICKHOUSE_MIGRATE_DIRECTORY"
    DEFAULT_MIGRATIONS_DIR = path.join("./migrations")

    databases = None
    migration_dir = None

    def init_config(self, migration_dir: Optional[str] = None, databases: Optional[List[str]] = None):
        self.databases = databases or env.list(self.DATABASES_ENV_VAR, subcast=str, default=None)
        self.migration_dir = migration_dir or env.str(self.DIRECTORY_ENV_VAR, default=self.DEFAULT_MIGRATIONS_DIR)
