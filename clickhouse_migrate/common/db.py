from typing import Any, Dict, List, Optional, Tuple

from clickhouse_driver import connect
from clickhouse_driver.dbapi import Connection

from clickhouse_migrate.common.meta import Singleton
from clickhouse_migrate.common.models.db import Database
from clickhouse_migrate.conf.settings import Settings


class DbRegister(metaclass=Singleton):
    """
    Singleton which handles connections with data storage
    """

    _pool: Dict[str, Database] = {}
    POOL_DEFAULT_NAME = "default"

    def setup_db(self):
        if self.db_instance is not None:
            return

        self.db_instance = Database(
            connection=connect(dsn=Settings().conn_str),
            is_in_cluster=Settings().is_in_cluster,
            cluster_name=Settings().cluster_name,
        )

    @property
    def db_instance(self) -> Optional[Database]:
        return self._pool.get(self.POOL_DEFAULT_NAME, None)

    @db_instance.setter
    def db_instance(self, db: Database):
        self._pool[self.POOL_DEFAULT_NAME] = db


def connection() -> Connection:
    return DbRegister().db_instance.connection


def execute(query: str, params: dict = None) -> List[Tuple[Any]]:
    if params is None:
        params = {}
    with connection().cursor() as cursor:
        cursor.execute(operation=query, parameters=params)
        return cursor.fetchall()
