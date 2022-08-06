from typing import Any, Dict, List, Optional, Tuple

from clickhouse_driver import connect
from clickhouse_driver.dbapi import Connection

from clickhouse_migrate.common.meta import Singleton
from clickhouse_migrate.common.models.db import Database, ReplicaSet
from clickhouse_migrate.conf.settings import Settings


class DbRegister(metaclass=Singleton):
    """
    Singleton which handles connections with data storage
    """

    _pool: Dict[str, ReplicaSet] = {}
    POOL_DEFAULT_NAME = "default"

    def setup_db(self):
        if self.replica_set is not None:
            return

        db_host_list = Settings().databases
        self.replica_set = ReplicaSet(
            connection=connect(db_host_list[0]),
            replicas=[Database(connection=connect(host)) for host in db_host_list],
        )

    @property
    def replica_set(self) -> Optional[ReplicaSet]:
        return self._pool.get(self.POOL_DEFAULT_NAME, None)

    @replica_set.setter
    def replica_set(self, replica_instance: ReplicaSet):
        self._pool[self.POOL_DEFAULT_NAME] = replica_instance


def connection() -> Connection:
    return DbRegister().replica_set.connection


def execute(query: str, params: dict = None) -> List[Tuple[Any]]:
    if params is None:
        params = {}
    with connection().cursor() as cursor:
        cursor.execute(operation=query, parameters=params)
        return cursor.fetchall()


def execute_for_replicas(query: str, params: dict = None):
    if params is None:
        params = {}

    for replica in DbRegister().replica_set.replicas:
        with replica.connection.cursor() as cursor:
            cursor.execute(operation=query, parameters=params)
            cursor.fetchall()
