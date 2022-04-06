import logging
from typing import Dict, List, Any, Tuple

from clickhouse_driver import connect
from clickhouse_driver.dbapi import Connection

from clickhouse_migrate.common.exceptions.db import UnknownInstanceError
from clickhouse_migrate.common.meta import Singleton
from clickhouse_migrate.common.models.db import Database, ReplicaSet
from clickhouse_migrate.conf.settings import Settings

logger = logging.getLogger(__name__)


class DbRegister(metaclass=Singleton):
    """
    Singleton which handles connections with data storage
    """

    _pool: Dict[str, ReplicaSet] = {}
    POOL_DEFAULT_NAME = "default"

    def setup_db(self):
        if self._pool.get(self.POOL_DEFAULT_NAME) is not None:
            return

        db_host_list = Settings().databases
        self._pool[self.POOL_DEFAULT_NAME] = ReplicaSet(
            connection=connect(db_host_list[0]),
            replicas=[Database(connection=connect(host)) for host in db_host_list],
        )

    def get_connection_instance(self) -> ReplicaSet:
        try:
            return self._pool[self.POOL_DEFAULT_NAME]
        except KeyError:
            logger.error(
                f"""Selected pool_name {self.POOL_DEFAULT_NAME} is not present in the register"""
            )
            raise UnknownInstanceError


def connection() -> Connection:
    return DbRegister().get_connection_instance().connection


def execute(query: str, params: dict = None) -> List[Tuple[Any]]:
    if params is None:
        params = {}
    with connection().cursor() as cursor:
        cursor.execute(operation=query, parameters=params)
        return cursor.fetchall()


def execute_for_replicas(query: str, params: dict = None):
    replica_set = DbRegister().get_connection_instance()
    if not isinstance(replica_set, ReplicaSet):
        logger.warning(
            """You are trying to execute the query for the ReplicaSet 
            but the selected instance is a single Database instance"""
        )
        return execute(query=query, params=params)

    if params is None:
        params = {}

    for replica in replica_set.replicas:
        with replica.connection.cursor() as cursor:
            cursor.execute(operation=query, parameters=params)
            cursor.fetchall()
