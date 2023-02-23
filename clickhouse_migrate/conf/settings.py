from os import path
from typing import Optional

from envparse import env

from clickhouse_migrate.common.meta import Singleton

env.read_envfile()


class Settings(metaclass=Singleton):
    CH_CONN_STR_VARIABLE = "CLICKHOUSE_CONN_STR"
    DIRECTORY_ENV_VAR = "CLICKHOUSE_MIGRATE_DIRECTORY"
    IS_IN_CLUSTER = "IS_IN_CLUSTER"
    CLUSTER_NAME = "CLUSTER_NAME"
    DEFAULT_MIGRATIONS_DIR = path.join("./migrations")

    conn_str = None
    migration_dir = None
    is_in_cluster = None
    cluster_name = None

    def init_config(
        self,
        migration_dir: Optional[str] = None,
        conn_str: str = None,
        is_in_cluster: bool = False,
        cluster_name: str = None,
    ):
        self.conn_str = conn_str or env.str(self.CH_CONN_STR_VARIABLE, default=None)
        self.migration_dir = migration_dir or env.str(self.DIRECTORY_ENV_VAR, default=self.DEFAULT_MIGRATIONS_DIR)
        self.is_in_cluster = is_in_cluster or env.bool(self.IS_IN_CLUSTER, default=False)
        self.cluster_name = cluster_name or env.str(self.CLUSTER_NAME)
